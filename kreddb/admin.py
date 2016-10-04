from django.contrib import admin

from kreddb import models


class ModelFamilyInline(admin.StackedInline):
    model = models.ModelFamily
    extra = 1
    show_change_link = True


class GenerationInline(admin.StackedInline):
    model = models.Generation
    extra = 1
    show_change_link = True


class CarModelInline(admin.StackedInline):
    model = models.CarModel
    extra = 1
    show_change_link = True


class CarImageInline(admin.StackedInline):
    model = models.CarImage
    extra = 1
    fields = ('image', 'main', )


class ModificationInline(admin.StackedInline):
    model = models.Modification
    extra = 0
    show_change_link = True
    readonly_fields = ('car_make', 'model_family', 'generation', 'old_id', )


class CarMakeAdmin(admin.ModelAdmin):
    inlines = [
        ModelFamilyInline,
    ]


class ModelFamilyAdmin(admin.ModelAdmin):
    inlines = [
        GenerationInline,
    ]

    readonly_fields = ('car_make',)


class GenerationAdmin(admin.ModelAdmin):
    inlines = [
        CarModelInline
    ]

    readonly_fields = ('car_make', 'model_family', 'year_start',)


class CarModelAdmin(admin.ModelAdmin):
    inlines = [
        CarImageInline,
        ModificationInline,
    ]

    readonly_fields = ('generation', )


class ModificationAdmin(admin.ModelAdmin):
    readonly_fields = ('car_make', 'model_family', 'generation', 'body_id', 'generation_id')


class CarImageAdmin(admin.ModelAdmin):
    readonly_fields = ('generation', 'body', 'body_id', 'generation_id')


admin.site.register(models.CarMake, CarMakeAdmin)
admin.site.register(models.ModelFamily, ModelFamilyAdmin)
admin.site.register(models.Generation, GenerationAdmin)
admin.site.register(models.CarModel, CarModelAdmin)
admin.site.register(models.Body)
admin.site.register(models.Engine)
admin.site.register(models.Gear)
admin.site.register(models.Equipment)
admin.site.register(models.Feature)
admin.site.register(models.Modification, ModificationAdmin)
admin.site.register(models.EquipmentCost)
admin.site.register(models.ModificationFeatures)
admin.site.register(models.CarImage, CarImageAdmin)
