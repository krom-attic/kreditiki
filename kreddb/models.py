from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.urlresolvers import reverse
from django.db import models

SAFE_TRANSLATION = str.maketrans(' &+:,/«»³®`×', '----_\\""3R\'x')


class CarMake(models.Model):
    name = models.CharField(db_index=True, max_length=127)
    # old_id = models.IntegerField(unique=True, null=True)
    display = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def filter_url(self):
        return reverse('kreddb:list_car_models', kwargs={'car_make': self.name})

    @classmethod
    def get_by_name(cls, name):
        return cls.objects.get(name=name)
    #
    # @classmethod
    # def get_by_old_id(cls, old_id):
    #     return cls.objects.get(old_id=old_id)


class CarModel(models.Model):
    name = models.CharField(db_index=True, max_length=127)
    car_make = models.ForeignKey(CarMake)
    # old_id = models.IntegerField(unique=True, null=True)
    display = models.BooleanField(default=False)

    def __str__(self):
        return self.car_make.name + ' ' + self.name

    @property
    def safe_name(self):
        return self.name.replace('/', '%')

    def filter_url(self):
        return reverse('kreddb:list_modifications',
                       kwargs=dict(car_make=self.car_make.name, car_model=self.safe_name))

    @classmethod
    def get_by_safe_name(cls, safe_name, car_make):
        return cls.objects.get(name=safe_name.replace('%', '/'), car_make=car_make)

    @classmethod
    def get_by_name(cls, name, car_make):
        return cls.objects.get(name=name, car_make=car_make)
    #
    # @classmethod
    # def get_by_old_id(cls, old_id):
    #     return cls.objects.get(old_id=old_id)


class Generation(models.Model):
    name = models.CharField(max_length=127, blank=True)
    car_make = models.ForeignKey(CarMake)
    car_model = models.ForeignKey(CarModel)
    year_start = models.IntegerField()
    year_end = models.IntegerField()
    # old_id = models.IntegerField(unique=True, null=True)

    class Meta:
        ordering = ['-year_start']
        unique_together = (('name', 'car_model', 'year_start', 'year_end'),)

    def __str__(self):
        return self.car_make.name + ' ' + self.car_model.name + ' ' + self.name

    @property
    def url_kwargs(self):
        url_kwargs = {'car_make': self.car_make.name, 'car_model': self.car_model.name, 'name': self.name, 'body': '-',
                      'engine': '-', 'gear': '-'}
        return url_kwargs

    def get_absolute_url(self):
        return reverse('kreddb:list_modifications', kwargs=self.url_kwargs)

    @classmethod
    def get_for_model(cls, car_make, car_model, **kwargs):
        return cls.objects.get(car_make=car_make, car_model=car_model, **kwargs)

    @classmethod
    def get_by_name_and_year(cls, car_model, year_start, year_end, name):
        try:
            return cls.objects.get(car_model=car_model, year_start=year_start, year_end=year_end, name=name)
        except MultipleObjectsReturned as e:
            print('MOR with {}, {}, {}, {}'.format(car_model, year_start, year_end, name))
            raise e
        except ObjectDoesNotExist as e:
            print('DNE with {}, {}, {}, {}'.format(car_model, year_start, year_end, name))
            raise e


    # @classmethod
    # def get_by_old_id(cls, old_id):
    #     return cls.objects.get(old_id=old_id)


class Body(models.Model):
    name = models.CharField(db_index=True, max_length=127)
    # old_id = models.IntegerField(unique=True, null=True)

    def __str__(self):
        return self.name

    @classmethod
    def get_by_name(cls, name):
        return cls.objects.get(name=name)

    # @classmethod
    # def get_by_old_id(cls, old_id):
    #     return cls.objects.get(old_id=old_id)


class Engine(models.Model):
    name = models.CharField(db_index=True, max_length=127)
    # old_id = models.IntegerField(unique=True, null=True)

    @classmethod
    def get_by_name(cls, name):
        return cls.objects.get(name=name)

    # @classmethod
    # def get_by_old_id(cls, old_id):
    #     return cls.objects.get(old_id=old_id)


class Gear(models.Model):
    name = models.CharField(db_index=True, max_length=127)
    # old_id = models.IntegerField(unique=True, null=True)

    @classmethod
    def get_by_name(cls, name):
        return cls.objects.get(name=name)

    # @classmethod
    # def get_by_old_id(cls, old_id):
    #     return cls.objects.get(old_id=old_id)


class Equipment(models.Model):
    # используются на фронте, не должны конфликтовать с характеристиками
    GROUP_CHOICES = (
        ('SF', 'Безопасность'),
        ('CF', 'Комфорт'),
        ('VW', 'Обзор'),
        ('IN', 'Салон'),
        ('MM', 'Мультимедиа'),
        ('CJ', 'Защита от угона'),
        ('EX', 'Экстерьер'),
    )
    name = models.CharField(db_index=True, max_length=255)
    group = models.CharField(max_length=2, choices=GROUP_CHOICES)
    rank = models.SmallIntegerField()

    class Meta:
        unique_together = (('group', 'rank'),)


class Feature(models.Model):
    # используются на фронте, не должны конфликтовать с оборудовнием
    GROUP_CHOICES = (
        ('GE', 'Общая информация'),
        ('SR', 'Безопасность'),
        ('EC', 'Эксплуатационные показатели'),
        ('EN', 'Двигатель'),
        ('GR', 'Трансмиссия'),
        ('SZ', 'Размеры в мм'),
        ('VM', 'Объем и масса'),
        ('SB', 'Подвеска и тормоза'),
    )
    name = models.CharField(db_index=True, max_length=255)
    group = models.CharField(max_length=2, choices=GROUP_CHOICES)
    rank = models.SmallIntegerField()

    class Meta:
        unique_together = (('group', 'rank'),)


class Modification(models.Model):
    name = models.CharField(max_length=127, blank=True)
    # TODO удалить следующие два поля? это же дублирование!
    car_make = models.ForeignKey(CarMake)
    car_model = models.ForeignKey(CarModel, db_index=True)
    generation = models.ForeignKey(Generation)
    body = models.ForeignKey(Body)
    gear = models.ForeignKey(Gear)
    engine = models.ForeignKey(Engine)
    cost = models.IntegerField(blank=True, null=True)
    equipment = models.ManyToManyField(Equipment, through='EquipmentCost')
    features = models.ManyToManyField(Feature, through='ModificationFeatures')
    old_id = models.IntegerField(unique=True, blank=True, null=True)

    @property
    def safe_name(self):
        return self.name.replace('/', '%')

    def get_absolute_url(self):
        mod_params = {
            'car_make': self.car_make.name,
            'car_model': self.car_model.safe_name,
            'generation': self.generation.name,
            'body': self.body.name,
            'gear': self.gear.name,
            'engine': self.engine.name,
            'gen_year_start': self.generation.year_start,
            'gen_year_end': self.generation.year_end,
            'complect': self.safe_name,
        }
        if self.cost is None:
            mod_params.update({'mod_id': self.id})
        else:
            mod_params.update({'cost': self.cost})
        # try:
        url = reverse('kreddb:view_modification', kwargs=mod_params)
        # except Exception as e:
        #     print(e.__str__())
        #     url = ''
        return url

    @classmethod
    def get_by_params(cls, generation, body, gear, engine, cost, name):
        # TODO Это не будет работать!!! Так уникальную модификацию не определить!!!
        try:
            return cls.objects.get(generation=generation, body=body, gear=gear, engine=engine, cost=cost, name=name)
        except MultipleObjectsReturned as e:
            print('MOR with {}, {}, {}, {}, {}, {}'.format(generation, body, gear, engine, cost, name))
            raise e
        except ObjectDoesNotExist as e:
            print('DNE with {}, {}, {}, {}, {}, {}'.format(generation, body, gear, engine, cost, name))
            raise e

    # TODO подумать над названием и сигнатурой метода
    @classmethod
    def get_by_name_and_gen(cls, **kwargs):
        # может вернуть несколько объектов!
        try:
            modification = cls.objects.get(**kwargs)
        except MultipleObjectsReturned as e:
            raise e
        return modification

    @classmethod
    def get_by_old_id(cls, old_id):
        return cls.objects.get(old_id=old_id)


class EquipmentCost(models.Model):
    modification = models.ForeignKey(Modification)
    equipment = models.ForeignKey(Equipment)
    cost = models.IntegerField()

    class Meta:
        unique_together = (('modification', 'equipment'),)


class ModificationFeatures(models.Model):
    modification = models.ForeignKey(Modification)
    feature = models.ForeignKey(Feature)
    value = models.CharField(max_length=127)

    class Meta:
        unique_together = (('modification', 'feature'),)


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


# class BodyOld(models.Model):
#     name = models.CharField(unique=True, max_length=253)
#
#     class Meta:
#         managed = False
#         db_table = 'body'
#
#     def __str__(self):
#         return self.name
#
#     # @property
#     # def safe_name(self):
#     #     try:
#     #         return self.bodycustom.safename
#     #     except ObjectDoesNotExist as e:
#     #         model_custom = BodyCustom(body_ptr=self, safename=self.name.translate(SAFE_TRANSLATION))
#     #         model_custom.save_base(raw=True)  # Обход тикета 7623
#     #         return model_custom.safename
#
#     @classmethod
#     def get_by_name(cls, name):
#         return cls.objects.get(name=name)


# class BodyCustom(BodyOld):
#     safename = models.CharField(blank=True, max_length=100, db_index=True)


# class Mark(models.Model):
#     name = models.CharField(unique=True, max_length=253)
#     group_name = models.CharField(max_length=253)
#     url = models.CharField(max_length=253)
#     count = models.IntegerField()
#
#     class Meta:
#         managed = False
#         db_table = 'mark'
#         ordering = ['name']
#
#     def __str__(self):
#         return self.name
#
#     def filter_url(self):
#         # try:
#         #     safename = self.markcustom.safename
#         # except ObjectDoesNotExist as e:
#         #     custom_mark = MarkCustom(mark_ptr=self, safename=self.name.translate(SAFE_TRANSLATION))
#         #     custom_mark.save_base(raw=True)  # Обход тикета 7623
#         #     safename = custom_mark.safename
#         return reverse('kreddb:list_car_models', kwargs={'car_make': self.name})
#
#     @classmethod
#     def get_by_name(cls, name):
#         return cls.objects.get(name=name)
#
#     # @classmethod
#     # def get_by_safe_name(cls, safe_name):
#     #     return MarkCustom.objects.get(safename=safe_name).mark_ptr


# class MarkCustom(Mark):
#     safename = models.CharField(blank=True, max_length=100)
#
#     class Meta:
#         managed = True


# class CarModelOld(models.Model):
#     name = models.CharField(unique=True, max_length=253)
#     generation_count = models.CharField(max_length=253, blank=True)
#     mark = models.ForeignKey(Mark)
#     url = models.CharField(max_length=253)
#     bottom_age = models.IntegerField(null=True, blank=True)
#     top_age = models.IntegerField(null=True, blank=True)
#
#     class Meta:
#         managed = False
#         db_table = 'model'
#
#     @property
#     def safe_name(self):
#         return self.name.replace('/', '%')
#
#     def filter_url(self):
#         return reverse('kreddb:list_modifications',
#                        kwargs=dict(car_make=self.mark.name, car_model=self.safe_name))
#
#     @classmethod
#     def get_by_name(cls, name, mark):
#         return cls.objects.get(name=name, mark=mark)
#
#     @classmethod
#     def get_by_safe_name(cls, safe_name, mark):
#         return cls.objects.get(name=safe_name.replace('%', '/'), mark=mark)


# class CarModelCustom(CarModelOld):
#     safename = models.CharField(blank=True, max_length=100, db_index=True)


# class GenerationOld(models.Model):
#     name = models.CharField(max_length=253)
#     cost = models.CharField(max_length=253)
#     car_model = models.ForeignKey(CarModelOld, db_column='model_id')
#     mark = models.ForeignKey(Mark)
#     url = models.CharField(unique=True, max_length=253)
#     generation = models.CharField(max_length=253, blank=True)
#     bottom_age = models.IntegerField()
#     top_age = models.IntegerField()
#     # safename = models.CharField(blank=True, max_length=100, db_index=True)
#
#     class Meta:
#         managed = False
#         db_table = 'generation'
#         ordering = ['-bottom_age']
#
#     @property
#     def safe_name(self):
#         """
#         Костыль для работы с оригинальной базой, где вместо пустых значений указано None
#         """
#         if self.generation is None:
#             return ''
#         else:
#             return self.generation
#
#     @property
#     def url_kwargs(self):
#         url_kwargs = {'mark': self.mark.name, 'car_model': self.car_model.name, 'generation': self.generation, 'body': '-',
#                       'engine': '-', 'gear': '-'}
#         return url_kwargs
#
#     def get_absolute_url(self):
#         return reverse('kreddb:list_modifications', kwargs=self.url_kwargs)
#
#     @classmethod
#     def get_for_model(cls, mark, car_model, **kwargs):
#         return cls.objects.get(mark=mark, car_model=car_model, **kwargs)
#
#     #
#     # @property
#     # def generation(self):
#     #     if self._generation:
#     #         return self._generation
#     #     else:
#     #         return ' '  # TODO Used in url, hence should be not empty
#     #
#     # @generation.setter
#     # def generation(self, value):
#     #     self._generation = value


# class EngineOld(models.Model):
#     name = models.CharField(unique=True, max_length=253)
#
#     class Meta:
#         managed = False
#         db_table = 'engine'
#
#     # @property
#     # def safe_name(self):
#     #     try:
#     #         return self.enginecustom.safename
#     #     except ObjectDoesNotExist as e:
#     #         model_custom = EngineCustom(engine_ptr=self, safename=self.name.translate(SAFE_TRANSLATION))
#     #         model_custom.save_base(raw=True)  # Обход тикета 7623
#     #         return model_custom.safename
#
#     @classmethod
#     def get_by_name(cls, name):
#         return cls.objects.get(name=name)


# class EngineCustom(EngineOld):
#     safename = models.CharField(blank=True, max_length=100, db_index=True)


# class GearOld(GearDB):
#
#     class Meta:
#         proxy = True


# class ModificationOld(models.Model):
#     name = models.CharField(max_length=253)
#     url = models.CharField(unique=True, max_length=253)
#     gear = models.ForeignKey(GearDB)
#     engine = models.ForeignKey(EngineOld)
#     mark = models.ForeignKey(Mark)
#     car_model = models.ForeignKey(CarModelOld, db_column='model_id')
#     generation = models.ForeignKey(GenerationOld)
#     complects_url = models.CharField(max_length=253, blank=True)
#     cost = models.CharField(max_length=253, blank=True, null=True)
#     body = models.ForeignKey(BodyOld)
#     equipment_name = models.CharField(max_length=253, blank=True)
#     # safename = models.CharField(blank=True, max_length=100, db_index=True)
#
#     class Meta:
#         managed = False
#         db_table = 'modification'
#
#     @property
#     def safe_name(self):
#         return self.equipment_name.replace('/', '%')
#
#     def get_absolute_url(self):
#         mod_params = {
#             'car_make': self.mark.name,
#             'car_model': self.car_model.safe_name,
#             'generation': self.generation.safe_name,
#             'gen_year_start': self.generation.top_age,
#             'gen_year_end': self.generation.bottom_age,
#             'body': self.body.name,
#             'engine': self.engine.name,
#             'gear': self.gear.name,
#             'complect': self.safe_name,
#         }
#         if self.cost is None:
#             mod_params.update({'mod_id': self.id})
#         else:
#             mod_params.update({'cost': self.cost})
#         # try:
#         url = reverse('kreddb:view_modification', kwargs=mod_params)
#         # except Exception as e:
#         #     print(e.__str__())
#         #     url = ''
#         return url
#
#     # TODO подумать над названием и сигнатурой метода
#     @classmethod
#     def get_by_name_and_gen(cls, **kwargs):
#         # может вернуть несколько объектов!
#         try:
#             modification = cls.objects.get(**kwargs)
#         except MultipleObjectsReturned as e:
#             raise e
#         return modification


# class KredModification(Modification):
#     tie_braker = models.SmallIntegerField(null=True, blank=True)


# class EquipmentDict(models.Model):
#     name = models.CharField(max_length=253)
#     cost = models.IntegerField()
#
#     class Meta:
#         managed = False
#         db_table = 'equipment_dict'
#         unique_together = (('name', 'cost'),)


# class EquipmentLk(models.Model):
#     equipment_dict = models.ForeignKey(EquipmentDict)
#     modification = models.ForeignKey(ModificationOld)
#
#     class Meta:
#         managed = False
#         db_table = 'equipment_lk'
#         unique_together = (('modification', 'equipment_dict'),)


# class FeatureDict(models.Model):
#     name = models.CharField(max_length=253)
#     value = models.CharField(max_length=253)
#
#     class Meta:
#         managed = False
#         db_table = 'feature_dict'
#         unique_together = (('name', 'value'),)


# class FeatureLk(models.Model):
#     feature_dict = models.ForeignKey(FeatureDict)
#     modification = models.ForeignKey(ModificationOld)
#
#     class Meta:
#         managed = False
#         db_table = 'feature_lk'
#         unique_together = (('modification', 'feature_dict'),)
