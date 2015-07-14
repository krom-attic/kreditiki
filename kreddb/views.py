from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from kreddb import models


class MarkListView(ListView):
    model = models.Mark


class NameFilterMixin:
    _filter_object = None

    def get_queryset(self):
        queryset = super().get_queryset()
        self._filter_object = self.filter_model.objects.get(name=self.kwargs[self.filter_model.__name__.lower()])
        qs_filter = {self.filter_model.__name__.lower(): self._filter_object}
        return queryset.filter(**qs_filter)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.filter_model.__name__.lower()] = self._filter_object
        return context


class ModelListView(NameFilterMixin, ListView):
    model = models.Model
    filter_model = models.Mark


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
        self.filter_mark = models.Mark.get_by_name(self.kwargs['mark'])
        self.filter_model = models.Model.get_by_name(self.kwargs['model'], self.filter_mark)
        qs_filter = {'model': self.filter_model}
        if 'generation' in self.kwargs and self.kwargs['generation'] != '-':
            self.filter_generation = models.Generation.get_by_name(self.kwargs['generation'], self.filter_mark, self.filter_model)
            qs_filter.update({'generation': self.filter_generation})
        if 'modification' in self.kwargs and self.kwargs['modification'] != '-':
            self.filter_modification = self.kwargs['modification']
            qs_filter.update({'equipment_name': self.filter_modification})
        if 'body' in self.kwargs and self.kwargs['body'] != '-':
            self.filter_body = models.Body.objects.get(name=self.kwargs['body'])
            qs_filter.update({'body': self.filter_body})
        if 'engine' in self.kwargs and self.kwargs['engine'] != '-':
            self.filter_engine = models.Engine.objects.get(name=self.kwargs['engine'])
            qs_filter.update({'engine': self.filter_engine})
        if 'gear' in self.kwargs and self.kwargs['gear'] != '-':
            self.filter_gear = models.Gear.objects.get(name=self.kwargs['gear'])
            qs_filter.update({'gear': self.filter_gear})
        return queryset.filter(**qs_filter)

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
    # TODO сделать тайбрейкер
    # ВНИМАНИЕ! Создавать tie_braker ТОЛЬКО если модификация действительно неуникальна
    model = models.Modification
    mark = None
    car_model = None
    generation = None
    modification = None
    body = None
    engine = None
    gear = None

    def get(self, request, *args, **kwargs):
        self.mark = models.Mark.get_by_name(self.kwargs['mark'])
        self.car_model = models.Model.get_by_name(self.kwargs['model'], self.mark)
        if self.kwargs['generation'] == 'None':
            self.kwargs['generation'] = None
        try:
            self.generation = models.Generation.get_by_name(self.kwargs['generation'], self.mark, self.car_model)
        except ObjectDoesNotExist as e:
            print(self.kwargs['generation'].encode(), self.mark.id, self.model.id)
        self.modification = self.kwargs['modification']
        self.body = models.Body.objects.get(name=self.kwargs['body'])
        self.engine = models.Engine.objects.get(name=self.kwargs['engine'])
        self.gear = models.Gear.objects.get(name=self.kwargs['gear'])
        qs_filter = {'generation': self.generation, 'equipment_name': self.modification,
                     'body': self.body, 'engine': self.engine, 'gear': self.gear}
        try:
            self.object = models.Modification.objects.get(**qs_filter)
        except MultipleObjectsReturned as e:
            raise e

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context.get('modification').cost:
            context['loan'] = int(context.get('modification').cost.replace('\u2009', ''))
        else:
            context['loan'] = None
        return context