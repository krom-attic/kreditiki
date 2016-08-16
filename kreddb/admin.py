from django.contrib import admin

from kreddb import models


class CarModelInline(admin.StackedInline):
    model = models.CarModel
    extra = 1
    show_change_link = True


class GenerationInline(admin.StackedInline):
    model = models.Generation
    extra = 1
    show_change_link = True


class GenerationImageInline(admin.StackedInline):
    model = models.GenerationImage
    extra = 1


class ModificationInline(admin.StackedInline):
    model = models.Modification
    extra = 0
    show_change_link = True
    readonly_fields = ('car_make', 'car_model')


class CarMakeAdmin(admin.ModelAdmin):
    inlines = [
        CarModelInline,
    ]


class CarModelAdmin(admin.ModelAdmin):
    inlines = [
        GenerationInline,
    ]

    readonly_fields = ('car_make',)


class GenerationAdmin(admin.ModelAdmin):
    inlines = [
        GenerationImageInline,
        ModificationInline,
    ]

    readonly_fields = ('car_make', 'car_model', 'year_start',)


class ModificationAdmin(admin.ModelAdmin):
    readonly_fields = ('car_make', 'car_model', 'generation',)


admin.site.register(models.CarMake, CarMakeAdmin)
admin.site.register(models.CarModel, CarModelAdmin)
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
