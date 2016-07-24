from django.contrib import admin

from kreddb import models


class GenerationImageInline(admin.StackedInline):
    model = models.GenerationImage


class GenerationAdmin(admin.ModelAdmin):
    inlines = [
        GenerationImageInline,
    ]

admin.site.register(models.CarMake)
admin.site.register(models.CarModel)
admin.site.register(models.Generation, GenerationAdmin)
admin.site.register(models.Body)
admin.site.register(models.Engine)
admin.site.register(models.Gear)
admin.site.register(models.Equipment)
admin.site.register(models.Feature)
admin.site.register(models.Modification)
admin.site.register(models.EquipmentCost)
admin.site.register(models.ModificationFeatures)
admin.site.register(models.GenerationImage)
