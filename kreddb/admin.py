from django.contrib import admin

from kreddb import models

# старьё
admin.site.register(models.Mark)
admin.site.register(models.CarModel)

# новьё
admin.site.register(models.CarMake)
admin.site.register(models.CarModelNew)
