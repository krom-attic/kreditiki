import json
import random

from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View

from rest_framework import response, views, viewsets

from kreddb import models
from kreddb.serializers import CarModelSerializer


# Вывод списка марок


class CarMakeListView(ListView):
    model = models.CarMake

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['car_makes'] = models.CarMake.objects.all()
    #     context['car_makes_list'] = list(context['car_makes'].values_list('name', flat=True))
    #     return context


# Вывод списка моделей


class CarModelListView(ListView):
    model = models.CarModel

    def __init__(self, **kwargs):
        self.car_make = None
        super().__init__(**kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        car_make_name = self.kwargs['car_make']
        self.car_make = models.CarMake.get_by_name(car_make_name)
        return queryset.filter(car_make=self.car_make)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['car_make'] = self.car_make
        # Это - заглушка, пока нет нормальных данных по картинкам
        stub_pics = [
            "http://toyota-tula.ru/images/88/common/all_new_toyota_camry_exterior.jpg",
            "http://i.ytimg.com/vi/_DnbTjf2VtA/maxresdefault.jpg",
            "http://recyclemag.ru/wp-content/uploads/2015/10/01-bmw-zagato-coupe.jpg",
            "http://carrrsmag.com/data_images/makes/audi/audi-01.jpg",
            "http://auto.sibkray.ru/images/uploads/autoproizv/skoda_rapid/skoda_7.jpg",
            "http://i.ytimg.com/vi/WV0XxP3kaic/maxresdefault.jpg",
        ]
        for car_model in context.get('carmodel_list', []):
            car_model.main_img_url = random.choice(stub_pics)
        return context


class CarModelListAPIView(View):
    def get(self, request, *args, **kwargs):
        car_make_name = kwargs['car_make']
        car_make = models.CarMake.get_by_name(car_make_name)
        # TODO раз уж мы получили объект марки, то для оптимизации его id можно будет передать на страницу
        car_models = list(models.CarModel
                          .objects
                          .filter(car_make=car_make)
                          .values_list('name', flat=True)
                          .order_by('name'))

        return HttpResponse(json.dumps(car_models))


# Обработчик селектора


class CarSelectorDispatchView(View):
    def dispatch(self, request, *args, **kwargs):
        car_make = request.GET.get('carmake')
        car_model = request.GET.get('carmodel')
        if car_make:
            if car_model:
                return redirect('kreddb:list_modifications', car_make=car_make, car_model=car_model.replace('/', '%'))
            else:
                return redirect('kreddb:list_car_models', car_make=car_make)
        else:
            print('Nothing OK')
        return super().dispatch(request, *args, **kwargs)


# Вывод списка модификаций


class ModificationListView(ListView):
    # TODO сделать фильтры
    model = models.Modification

    def __init__(self, **kwargs):
        self.car_make = None
        self.car_model = None
        self.generation = None
        self.modification = None
        self.body = None
        self.engine = None
        self.gear = None
        super().__init__(**kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        _car_make = self.kwargs['car_make']
        self.car_make = models.CarMake.get_by_name(_car_make)
        _car_model = self.kwargs['car_model']
        self.car_model = models.CarModel.get_by_safe_name(_car_model, self.car_make)
        qs_filter = {'car_model': self.car_model}

        # if 'generation' in self.kwargs and self.kwargs['generation'] != '-':
        #     self.generation = models.Generation.get_by_name(self.kwargs['generation'], self.filter_mark, self.filter_model)
        #     qs_filter.update({'generation': self.generation})
        # TODO добавить фильтр по году поколения
        if 'modification' in self.kwargs and self.kwargs['modification'] != '-':
            self.modification = self.kwargs['modification']
            qs_filter.update({'name': self.modification})
        if 'body' in self.kwargs and self.kwargs['body'] != '-':
            self.body = models.Body.objects.get(name=self.kwargs['body'])
            qs_filter.update({'body': self.body})
        if 'engine' in self.kwargs and self.kwargs['engine'] != '-':
            self.engine = models.Engine.objects.get(name=self.kwargs['engine'])
            qs_filter.update({'engine': self.engine})
        if 'gear' in self.kwargs and self.kwargs['gear'] != '-':
            self.gear = models.Gear.objects.get(name=self.kwargs['gear'])
            qs_filter.update({'gear': self.gear})
        # на данный момент неактуально, но может пригодиться
        if self.kwargs.get('all'):
            return queryset.filter(**qs_filter)
        else:
            return queryset.filter(**qs_filter).exclude(cost=None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'car_make': self.car_make, 'car_model': self.car_model})
        if self.generation:
            context.update({'generation': self.generation})
        if self.modification:
            context.update({'equipment_name': self.modification})
        if self.body:
            context.update({'body': self.body})
        if self.engine:
            context.update({'engine': self.engine})
        if self.gear:
            context.update({'gear': self.gear})
        return context


class ModificationDataApiView(View):
    def get(self, request, *args, **kwargs):
        modification_id = kwargs['mod_id']
        # TODO добавить упорядочевание
        features = models.ModificationFeatures.objects.filter(modification_id=modification_id)
        feature_dict = {}
        for feature in features:
            feature_dict.setdefault(feature.feature.group, {}).update({feature.feature.name: feature.value})

        equipment = models.EquipmentCost.objects.filter(modification_id=modification_id)
        equipment_dict = dict()
        for piece in equipment:
            equipment_dict.setdefault(piece.equipment.group, {}).update({piece.equipment.name: piece.cost})

        return HttpResponse(json.dumps({
            'mod_id': modification_id,
            'features': feature_dict,
            'equipment': equipment_dict
        }))


class ModificationDetailView(DetailView):
    model = models.Modification

    def __init__(self):
        self.object = None
        # self.kwargs = {}
        super().__init__()
        self.name = None
        self.car_make = None
        self.car_model = None
        self.generation = None
        self.gen_year_start = None
        self.body = None
        self.gear = None
        self.engine = None
        self.cost = None

    def get(self, request, *args, **kwargs):
        self.name = self.kwargs['complect'].replace('%', '/')
        self.car_make = models.CarMake.get_by_name(self.kwargs['car_make'])
        self.car_model = models.CarModel.get_by_safe_name(self.kwargs['car_model'], self.car_make)
        generation_info = dict(year_start=self.kwargs['gen_year_start'])  # , year_end=self.kwargs['gen_year_end'])
        # if self.kwargs['generation'] == 'None':
        #     self.kwargs['generation'] = None
        if self.kwargs['generation']:
            generation_info['name'] = self.kwargs['generation']
        # TODO создать метод на модели поколения
        self.generation = models.Generation.get_for_model(self.car_make, self.car_model, **generation_info)
        self.body = models.Body.get_by_name(self.kwargs['body'])
        self.engine = models.Engine.get_by_name(self.kwargs['engine'])
        self.gear = models.Gear.objects.get(name=self.kwargs['gear'])
        if self.kwargs.get('cost'):
            self.cost = self.kwargs['cost']
            qs_kwargs = {'name': self.name, 'generation': self.generation, 'body': self.body,
                         'engine': self.engine, 'gear': self.gear, 'cost': self.cost}
            self.object = models.Modification.get_by_name_and_gen(**qs_kwargs)
        elif self.kwargs.get('mod_id'):
            # TODO а используется это сейчас где-то?
            self.object = models.Modification.objects.get(id=self.kwargs['mod_id'])
        else:
            raise Exception('Недостаточно данных для идентификации модификации')
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        creditcalc_context = {}
        # TODO переделать на проверку self.cost???
        modification = context.get('modification')
        if context.get('modification').cost:
            creditcalc_context['price'] = modification.cost
        else:
            creditcalc_context['price'] = None
        photo_urls = [car_image.image.url.rsplit('.', 1)
                      for car_image in modification.generation.carimage_set.filter(body=modification.body)]
        creditcalc_context['photos'] = [{'path': url[0], 'ext': url[1]} for url in photo_urls]
        creditcalc_context['car_name'] = '{} {}'.format(modification.car_make.name, modification.car_model.name)
        context['creditcalc'] = creditcalc_context
        return context


# Ниже - разобрать


# class NameFilterMixin:
#     _filter_object = None
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         self._filter_object = self.filter_model.objects.get(name=self.kwargs[self.filter_model.__name__.lower()])
#         qs_filter = {self.filter_model.__name__.lower(): self._filter_object}
#         return queryset.filter(**qs_filter)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context[self.filter_model.__name__.lower()] = self._filter_object
#         return context




# class GenerationListView(ListView):
#     model = models.GenerationOld
#     filter_mark = None
#     filter_model = None
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         self.filter_mark = models.Mark.get_by_name(self.kwargs['mark'])
#         self.filter_model = models.Model.get_by_name(self.kwargs['model'], self.filter_mark)
#         return queryset.filter(model=self.filter_model)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context.update({'mark': self.filter_mark, 'model': self.filter_model})
#         return context


# вроде нигде больше не использую
class ListModificationsAjaxView(View):
    def get(self, request, *args, **kwargs):
        _mark = request.GET['mark']
        mark = models.Mark.get_by_name(_mark)
        _car_model = request.GET['car_model']
        car_model = models.CarModelOld.get_by_name(_car_model, mark)
        modifications = [''] + list(models.ModificationOld.objects.exclude(cost=None).filter(mark=mark, car_model=car_model).values_list('name', flat=True))
        return JsonResponse({'result': modifications})


class SearchModificationsAjaxView(View):
    def get(self, request, *args, **kwargs):
        _mark = request.GET['mark']
        mark = models.Mark.get_by_name(_mark)
        _car_model = request.GET['car_model']
        car_model = models.CarModelOld.get_by_name(_car_model, mark)
        qs_filter = dict(mark=mark, car_model=car_model)
        _modification = request.GET.get('modification')
        if _modification:
            qs_filter.update(dict(name=_modification))
        modifications = models.ModificationOld.objects.exclude(cost=None).filter(**qs_filter)
        if len(modifications) == 1:
            new_url = modifications.get().get_absolute_url()
        else:
            new_url = car_model.filter_url()
        return JsonResponse({'result': new_url})


class CarModelViewSet(viewsets.ModelViewSet):
    lookup_field = 'name'
    queryset = models.CarModel.objects.filter(name__startswith="A")
    serializer_class = CarModelSerializer


class ListModificationsAPIView(views.APIView):
    def get(self, request, format=None, *args, **kwargs):
        _car_make = kwargs['mark']
        car_make = models.Mark.get_by_name(_car_make)
        _car_model = kwargs['car_model']
        car_model = models.CarModelOld.get_by_name(_car_model, car_make)
        modifications = list(models.ModificationOld.objects.exclude(cost=None).filter(mark=car_make, car_model=car_model).values_list('name', flat=True))

        return response.Response(modifications)
