import json

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import mail_managers
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, View

from kreddb import models
from kreddb.bl.image_works import get_car_main_images
from kreddb.bl.site_options import get_promo_items
from kreddb.models import cipher_id, decipher_id


class CarMakeListView(ListView):
    """Вывод списка марок"""
    model = models.CarMake

    def get_queryset(self):
        # можно не гонять дополнительные поля, но пока их мало (только display)
        return super().get_queryset().filter(display=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['promo'] = get_promo_items()
        except ObjectDoesNotExist:
            pass  # когда сайт не настроен, промо нет. ну и фиг с ним
        return context


class CarModelListView(ListView):
    """Вывод списка моделей"""
    model = models.CarModel

    def __init__(self, **kwargs):
        self.car_make = None
        super().__init__(**kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        car_make_name = self.kwargs['car_make']
        self.car_make = models.CarMake.get_by_name(car_make_name)
        # сдаётся мне, что следование структуре джанговских вьюшек менее правильно, чем вынос из контроллера логики,
        # связанной получением данных из бд...
        return queryset.filter(generation__car_make=self.car_make, display=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['car_make'] = self.car_make
        for car_model in context.get('carmodel_list', []):
            car_model.main_img_urls = get_car_main_images(car_model)
            car_model.get_price_per_day()
        return context


class CarModelListAPIView(View):
    def get(self, request, *args, **kwargs):
        car_make_name = kwargs['car_make']
        car_make = models.CarMake.get_by_name(car_make_name)
        # TODO возможно тут надо намекнуть джанге на подгрузку связанных записей
        car_models = models.CarModel.objects_actual.filter(model_family__car_make=car_make)
        car_models_list = [{
                               'id': cipher_id(str(car_model.id)),
                               'name': car_model.model_name
                           }
                           for car_model in car_models
                           ]

        return HttpResponse(json.dumps(car_models_list))


class CarSelectorDispatchView(View):
    """Обработчик селектора"""
    def dispatch(self, request, *args, **kwargs):
        car_make = request.GET.get('carmake')
        car_model_id = request.GET.get('carmodel')
        if car_make:
            if car_model_id:
                car_model = models.CarModel.objects.get(id=decipher_id(car_model_id))
                return redirect(car_model)
            else:
                return redirect('kreddb:list_model_families', car_make=car_make)
        else:
            # TODO заменить на логирование
            print('Nothing OK')
        return super().dispatch(request, *args, **kwargs)


class ModificationListView(ListView):
    """Вывод списка модификаций"""
    # TODO сделать фильтры
    model = models.Modification

    def __init__(self, **kwargs):
        self.car_model = None
        super().__init__(**kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()

        qs_filter = queryset.filter(car_model__id=decipher_id(self.kwargs['object_id']))

        # на данный момент неактуально, но может пригодиться
        if self.kwargs.get('all'):
            return qs_filter
        else:
            return qs_filter.exclude(cost=None)


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

    def get(self, request, *args, **kwargs):
        self.object = models.Modification.objects.get(pk=decipher_id(self.kwargs['object_id']))
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        creditcalc_context = {}
        modification = context.get('modification')
        if context.get('modification').cost:
            creditcalc_context['price'] = modification.cost
        else:
            creditcalc_context['price'] = None
        photo_urls = [car_image.image.url.rsplit('.', 1)
                      for car_image in modification.car_model.carimage_set.all()]
        creditcalc_context['photos'] = [{'path': url[0], 'ext': url[1]} for url in photo_urls]
        creditcalc_context['car_name'] = '{} {}'.format(modification.car_make.name, modification.model_family.name)
        context['creditcalc'] = creditcalc_context
        return context


class CreditApplicationView(View):
    # TODO проверить сигнатуру метода
    def post(self, request, *args, **kwargs):
        params = json.loads(request.body.decode())
        mail_managers(
            'Новая заявка на кредит',
            str(params),
        )
        return HttpResponse('OK')
