from django.contrib import admin

from kreddb import models


class GenerationImageInline(admin.StackedInline):
    model = models.GenerationImage


class GenerationAdmin(admin.ModelAdmin):
    inlines = [
        GenerationImageInline,
    ]

    readonly_fields = ('car_make',)

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context['adminform'].form.fields['car_model'].queryset = models.CarModel.objects.filter(
            car_make=context['original'].car_make
        )
        return super().render_change_form(request, context, add, change, form_url, obj)


class ModificationAdmin(admin.ModelAdmin):
    readonly_fields = ('car_make', 'car_model')

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context['adminform'].form.fields['generation'].queryset = models.Generation.objects.filter(
            car_model=context['original'].car_model
        )
        return super().render_change_form(request, context, add, change, form_url, obj)


admin.site.register(models.CarMake)
admin.site.register(models.CarModel)
admin.site.register(models.Generation, GenerationAdmin)
admin.site.register(models.Body)
admin.site.register(models.Engine)
admin.site.register(models.Gear)
admin.site.register(models.Equipment)
admin.site.register(models.Feature)
admin.site.register(models.Modification, ModificationAdmin)
admin.site.register(models.EquipmentCost)
admin.site.register(models.ModificationFeatures)
admin.site.register(models.GenerationImage)
