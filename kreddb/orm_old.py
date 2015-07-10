from django.db import models

class BodyDB(models.Model):
    name = models.CharField(unique=True, max_length=253)

    class Meta:
        managed = False
        db_table = 'body'


class MarkDB(models.Model):
    name = models.CharField(unique=True, max_length=253)
    group_name = models.CharField(max_length=253)
    url = models.CharField(max_length=253)
    count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'mark'


class EngineDB(models.Model):
    name = models.CharField(unique=True, max_length=253)

    class Meta:
        managed = False
        db_table = 'engine'


class GearDB(models.Model):
    name = models.CharField(unique=True, max_length=253)

    class Meta:
        managed = False
        db_table = 'gear'


