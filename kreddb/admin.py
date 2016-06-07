from django.contrib import admin

from kreddb import models

# старьё
# admin.site.register(models.Mark)
# admin.site.register(models.CarModelOld)

# новьё
admin.site.register(models.CarMake)
admin.site.register(models.CarModel)
admin.site.register(models.Generation)
admin.site.register(models.Body)
admin.site.register(models.Engine)
admin.site.register(models.Gear)
admin.site.register(models.Equipment)
admin.site.register(models.Feature)
admin.site.register(models.Modification)
admin.site.register(models.EquipmentCost)
admin.site.register(models.ModificationFeatures)
