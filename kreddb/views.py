import json
from pprint import pprint

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, View

from kreddb import models


def get_new_car_models(mark):
    return models.Modification.objects.exclude(cost=None).filter(mark=mark).values_list('car_model', flat=True).distinct()


class MarkListView(ListView):
    model = models.Mark

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        marks = models.Modification.objects.exclude(cost=None).values_list('mark', flat=True).distinct()
        context['mark_new_list'] = models.Mark.objects.filter(id__in=marks)
        return context

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


class CarModelListView(ListView):
    model = models.CarModel
    _filter_object = None

    def get_queryset(self):
        queryset = super().get_queryset()
        self._filter_object = models.MarkCustom.objects.get(safename=self.kwargs['mark']).mark_ptr
        _car_models = get_new_car_models(self._filter_object)
        return queryset.filter(id__in=_car_models)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mark'] = self._filter_object
        return context


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


class ModificationListView(ListView):
    # TODO сделать фильтры
    model = models.Modification
    filter_mark = None
    filter_model = None
    filter_generation = None
    filter_modification = None
    filter_body = None
    filter_engine = None
    filter_gear = None

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filter_mark = models.Mark.get_by_safe_name(self.kwargs['mark'])
        self.filter_model = models.CarModel.get_by_safe_name(self.kwargs['car_model'], self.filter_mark)
        qs_filter = {'car_model': self.filter_model}
        # if 'generation' in self.kwargs and self.kwargs['generation'] != '-':
        #     self.filter_generation = models.Generation.get_by_name(self.kwargs['generation'], self.filter_mark, self.filter_model)
        #     qs_filter.update({'generation': self.filter_generation})
        # TODO добавить фильтр по году поколения
        if 'modification' in self.kwargs and self.kwargs['modification'] != '-':
            self.filter_modification = self.kwargs['modification']
            qs_filter.update({'equipment_name': self.filter_modification})
        if 'body' in self.kwargs and self.kwargs['body'] != '-':
            self.filter_body = models.Body.objects.get(name=self.kwargs['body'])
            qs_filter.update({'body': self.filter_body})
        if 'engine' in self.kwargs and self.kwargs['engine'] != '-':
            self.filter_engine = models.EngineCustom.objects.get(name=self.kwargs['engine']).engine_ptr
            qs_filter.update({'engine': self.filter_engine})
        if 'gear' in self.kwargs and self.kwargs['gear'] != '-':
            self.filter_gear = models.Gear.objects.get(name=self.kwargs['gear'])
            qs_filter.update({'gear': self.filter_gear})
        if self.kwargs.get('all'):
            return queryset.filter(**qs_filter)
        else:
            return queryset.filter(**qs_filter).exclude(cost=None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'mark': self.filter_mark, 'model': self.filter_model})
        if self.filter_generation:
            context.update({'generation': self.filter_generation})
        if self.filter_modification:
            context.update({'equipment_name': self.filter_modification})
        if self.filter_body:
            context.update({'body': self.filter_body})
        if self.filter_engine:
            context.update({'engine': self.filter_engine})
        if self.filter_gear:
            context.update({'gear': self.filter_gear})
        return context


class ModificationDetailView(DetailView):
    model = models.Modification

    def __init__(self):
        super().__init__()
        self.mark = None
        self.car_model = None
        self.generation = None
        self.gen_year_start = None
        self.gen_year_end = None
        self.modification = None
        self.body = None
        self.engine = None
        self.gear = None
        self.cost = None

    def get(self, request, *args, **kwargs):
        self.mark = models.Mark.get_by_safe_name(self.kwargs['mark'])
        self.car_model = models.CarModel.get_by_safe_name(self.kwargs['car_model'], self.mark)
        generation_info = dict(top_age=self.kwargs['gen_year_start'], bottom_age=self.kwargs['gen_year_end'])
        # if self.kwargs['generation'] == 'None':
        #     self.kwargs['generation'] = None
        if self.kwargs['generation']:
            generation_info['safename'] = self.kwargs['generation']
        self.generation = models.Generation.get_for_model(self.mark, self.car_model, **generation_info)
        self.modification = self.kwargs['modification']
        self.body = models.Body.get_by_safe_name(self.kwargs['body'])
        self.engine = models.Engine.get_by_safe_name(self.kwargs['engine'])
        self.gear = models.Gear.objects.get(name=self.kwargs['gear'])
        if self.kwargs.get('cost'):
            self.cost = self.kwargs['cost']
            qs_filter = {'generation': self.generation, 'equipment_name': self.modification,
                         'body': self.body, 'engine': self.engine, 'gear': self.gear, 'cost': self.cost}
        elif self.kwargs.get('mod_id'):
            qs_filter = {'id': self.kwargs['mod_id']}
        else:
            raise Exception('Недостаточно данных для идентификации модификации')
        try:
            self.object = models.Modification.objects.get(**qs_filter)
        except MultipleObjectsReturned as e:
            raise e
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # TODO переделать на проверку self.cost
        if context.get('modification').cost:
            context['loan'] = context.get('modification').cost
        else:
            context['loan'] = None
        return context


class ListCarModelsAjaxView(View):
    def get(self, request, *args, **kwargs):
        _mark = request.GET['mark']
        mark = models.Mark.get_by_name(_mark)
        # TODO раз уж мы получили объект марки, то для оптимизации его id можно будет передать на страницу
        _car_models = get_new_car_models(mark)
        car_models = [''] + list(models.CarModel.objects.filter(id__in=_car_models).values_list('name', flat=True).order_by('name'))
        return JsonResponse({'result': car_models})


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
