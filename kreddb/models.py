from django.core.urlresolvers import reverse

from kreddb.orm_old import *

# если max_length=253, значит он выставлен автоматически


# NOT USED
# class User(models.Model):
#     ident = models.CharField(unique=True, max_length=253)
#     password = models.CharField(max_length=253, blank=True)
#
#     class Meta:
#         managed = False
#         db_table = 'user'


# NOT USED
# class Email(models.Model):
#     email = models.CharField(unique=True, max_length=253)
#     user = models.ForeignKey(User, db_column='user', blank=True, null=True)
#     verkey = models.CharField(max_length=253, blank=True)
#
#     class Meta:
#         managed = False
#         db_table = 'email'


class Body(BodyDB):

    class Meta:
        proxy = True

    def __str__(self):
        return self.name


class Mark(MarkDB):

    class Meta:
        proxy = True

    def __str__(self):
        return self.name

    def filter_url(self):
        return reverse('kreddb:list_models', kwargs={'mark': self.name})

    @classmethod
    def get_by_name(cls, name):
        return cls.objects.get(name=name)


class Model(models.Model):
    name = models.CharField(unique=True, max_length=253)
    generation_count = models.CharField(max_length=253, blank=True)
    mark = models.ForeignKey(MarkDB)
    url = models.CharField(max_length=253)
    bottom_age = models.IntegerField(null=True, blank=True)
    top_age = models.IntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'model'

    @property
    def url_kwargs(self):
        return {'mark': self.mark.name, 'model': self.name}

    def filter_url(self):
        return reverse('kreddb:list_modifications', kwargs=self.url_kwargs)

    @classmethod
    def get_by_name(cls, name, mark):
        return cls.objects.get(name=name, mark=mark)


class Generation(models.Model):
    name = models.CharField(max_length=253)
    cost = models.CharField(max_length=253)
    model = models.ForeignKey(Model)
    mark = models.ForeignKey(MarkDB)
    url = models.CharField(unique=True, max_length=253)
    generation = models.CharField(max_length=253, blank=True)
    bottom_age = models.IntegerField()
    top_age = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'generation'
        ordering = ['-bottom_age']

    @property
    def url_kwargs(self):
        url_kwargs = {'mark': self.mark.name, 'model': self.model.name, 'generation': self.generation, 'body': '-',
                      'engine': '-', 'gear': '-'}
        return url_kwargs

    def get_absolute_url(self):
        return reverse('kreddb:list_modifications', kwargs=self.url_kwargs)

    @classmethod
    def get_for_model(cls, mark, model, **kwargs):
        return cls.objects.get(mark=mark, model=model, **kwargs)

    #
    # @property
    # def generation(self):
    #     if self._generation:
    #         return self._generation
    #     else:
    #         return ' '  # TODO Used in url, hence should be not empty
    #
    # @generation.setter
    # def generation(self, value):
    #     self._generation = value


class Engine(EngineDB):

    class Meta:
        proxy = True


class Gear(GearDB):

    class Meta:
        proxy = True


class Modification(models.Model):
    name = models.CharField(max_length=253)
    url = models.CharField(unique=True, max_length=253)
    gear = models.ForeignKey(GearDB)
    engine = models.ForeignKey(EngineDB)
    mark = models.ForeignKey(MarkDB)
    model = models.ForeignKey(Model)
    generation = models.ForeignKey(Generation)
    complects_url = models.CharField(max_length=253, blank=True)
    cost = models.CharField(max_length=253, blank=True, null=True)
    body = models.ForeignKey(BodyDB)
    equipment_name = models.CharField(max_length=253, blank=True)

    class Meta:
        managed = False
        db_table = 'modification'

    @property
    def generation_name(self):
        name = self.generation.generation
        return name if name else ''

    def get_absolute_url(self):
        mod_params = {
            'mark': self.mark.name,
            'model': self.model.name,
            'generation': self.generation_name,
            'gen_year_start': self.generation.top_age,
            'gen_year_end': self.generation.bottom_age,
            'body': self.body.name,
            'engine': self.engine.name,
            'gear': self.gear.name,
            'modification': self.equipment_name,
        }
        if self.cost is None:
            mod_params.update({'mod_id': self.id})
        else:
            mod_params.update({'cost': self.cost})
        try:
            url = reverse('kreddb:view_modification', kwargs=mod_params)
        except Exception as e:
            print(e.__str__())
            url = ''
        return url

    @classmethod
    def get_by_name(cls, name, mark, model, generation):
        return cls.objects.get(equipment_name=name, mark=mark, model=model, generation=generation)


class KredModification(Modification):
    tie_braker = models.SmallIntegerField(null=True, blank=True)


class EquipmentDict(models.Model):
    name = models.CharField(max_length=253)
    cost = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'equipment_dict'
        unique_together = (('name', 'cost'),)


class EquipmentLk(models.Model):
    equipment_dict = models.ForeignKey(EquipmentDict)
    modification = models.ForeignKey(Modification)

    class Meta:
        managed = False
        db_table = 'equipment_lk'
        unique_together = (('modification', 'equipment_dict'),)


class FeatureDict(models.Model):
    name = models.CharField(max_length=253)
    value = models.CharField(max_length=253)

    class Meta:
        managed = False
        db_table = 'feature_dict'
        unique_together = (('name', 'value'),)


class FeatureLk(models.Model):
    feature_dict = models.ForeignKey(FeatureDict)
    modification = models.ForeignKey(Modification)

    class Meta:
        managed = False
        db_table = 'feature_lk'
        unique_together = (('modification', 'feature_dict'),)
