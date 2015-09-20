from django.db import models


class GearDB(models.Model):
    name = models.CharField(unique=True, max_length=253)

    class Meta:
        managed = False
        db_table = 'gear'


