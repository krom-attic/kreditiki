import json
from pprint import pprint

from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View

from rest_framework import response, views, viewsets

from kreddb import models
from kreddb.serializers import CarModelSerializer


# Вывод списка марок


class MarkListView(ListView):
    model = models.Mark

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        marks = models.Modification.objects.exclude(cost=None).values_list('mark', flat=True).distinct()
        context['car_makes_new'] = models.Mark.objects.filter(id__in=marks)
        context['car_makes_new_list'] = list(context['car_makes_new'].values_list('name', flat=True))
        return context


# Вывод списка моделей


def get_new_car_models(mark):
    return models.Modification.objects.exclude(cost=None).filter(mark=mark).values_list('car_model', flat=True).distinct()


class CarModelListView(ListView):
    model = models.CarModel

    def __init__(self, **kwargs):
        self.car_make = None
        super().__init__(**kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        _car_make = self.kwargs['car_make']
        self.car_make = models.Mark.get_by_name(_car_make)
        _car_models = get_new_car_models(self.car_make)
        return queryset.filter(id__in=_car_models)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['car_make'] = self.car_make
        return context


class CarModelListAPIView(views.APIView):
    # TODO убрать format?
    def get(self, request, format=None, *args, **kwargs):
        _car_make = kwargs['car_make']
        car_make = models.Mark.get_by_name(_car_make)
        _car_models = get_new_car_models(car_make)
        # TODO раз уж мы получили объект марки, то для оптимизации его id можно будет передать на страницу
        car_models = list(models.CarModel.objects.filter(id__in=_car_models).values_list('name', flat=True).order_by('name'))

        return response.Response(car_models)


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
        self.car_make = models.Mark.get_by_name(_car_make)
        _car_model = self.kwargs['car_model']
        self.car_model = models.CarModel.get_by_safe_name(_car_model, self.car_make)
        qs_filter = {'car_model': self.car_model}

        # if 'generation' in self.kwargs and self.kwargs['generation'] != '-':
        #     self.generation = models.Generation.get_by_name(self.kwargs['generation'], self.filter_mark, self.filter_model)
        #     qs_filter.update({'generation': self.generation})
        # TODO добавить фильтр по году поколения?
        if 'modification' in self.kwargs and self.kwargs['modification'] != '-':
            self.modification = self.kwargs['modification']
            qs_filter.update({'equipment_name': self.modification})
        if 'body' in self.kwargs and self.kwargs['body'] != '-':
            self.body = models.Body.objects.get(name=self.kwargs['body'])
            qs_filter.update({'body': self.body})
        if 'engine' in self.kwargs and self.kwargs['engine'] != '-':
            self.engine = models.EngineCustom.objects.get(name=self.kwargs['engine']).engine_ptr
            qs_filter.update({'engine': self.engine})
        if 'gear' in self.kwargs and self.kwargs['gear'] != '-':
            self.gear = models.Gear.objects.get(name=self.kwargs['gear'])
            qs_filter.update({'gear': self.gear})
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


class ModificationDetailView(DetailView):
    model = models.Modification

    def __init__(self):
        self.object = None
        # self.kwargs = {}
        super().__init__()
        self.car_make = None
        self.car_model = None
        self.generation = None
        self.gen_year_start = None
        self.gen_year_end = None
        self.complect = None
        self.body = None
        self.engine = None
        self.gear = None
        self.cost = None

    def get(self, request, *args, **kwargs):
        self.car_make = models.Mark.get_by_name(self.kwargs['car_make'])
        self.car_model = models.CarModel.get_by_safe_name(self.kwargs['car_model'], self.car_make)
        generation_info = dict(top_age=self.kwargs['gen_year_start'], bottom_age=self.kwargs['gen_year_end'])
        # if self.kwargs['generation'] == 'None':
        #     self.kwargs['generation'] = None
        if self.kwargs['generation']:
            generation_info['generation'] = self.kwargs['generation']
        # TODO создать метод на модели поколения
        self.generation = models.Generation.get_for_model(self.car_make, self.car_model, **generation_info)
        self.complect = self.kwargs['complect'].replace('%', '/')
        self.body = models.Body.get_by_name(self.kwargs['body'])
        self.engine = models.Engine.get_by_name(self.kwargs['engine'])
        self.gear = models.Gear.objects.get(name=self.kwargs['gear'])
        if self.kwargs.get('cost'):
            self.cost = self.kwargs['cost']
            qs_kwargs = {'equipment_name': self.complect, 'generation': self.generation, 'body': self.body,
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
        creditcalc_context['photos'] = [
            static('kreddb/img/toyota-camry-1.jpg'),
            static('kreddb/img/toyota-camry-2.jpg'),
            static('kreddb/img/toyota-camry-3.jpg'),
        ]
        creditcalc_context['car_name'] = '{} {}'.format(modification.mark.name, modification.car_model.name)
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
#     model = models.Generation
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
        car_model = models.CarModel.get_by_name(_car_model, mark)
        modifications = [''] + list(models.Modification.objects.exclude(cost=None).filter(mark=mark, car_model=car_model).values_list('name', flat=True))
        return JsonResponse({'result': modifications})


class SearchModificationsAjaxView(View):
    def get(self, request, *args, **kwargs):
        _mark = request.GET['mark']
        mark = models.Mark.get_by_name(_mark)
        _car_model = request.GET['car_model']
        car_model = models.CarModel.get_by_name(_car_model, mark)
        qs_filter = dict(mark=mark, car_model=car_model)
        _modification = request.GET.get('modification')
        if _modification:
            qs_filter.update(dict(name=_modification))
        modifications = models.Modification.objects.exclude(cost=None).filter(**qs_filter)
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
        car_model = models.CarModel.get_by_name(_car_model, car_make)
        modifications = list(models.Modification.objects.exclude(cost=None).filter(mark=car_make, car_model=car_model).values_list('name', flat=True))

        return response.Response(modifications)
