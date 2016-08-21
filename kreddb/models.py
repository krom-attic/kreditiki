import json

from PIL import Image
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.urlresolvers import reverse
from django.db import models

SAFE_TRANSLATION = str.maketrans(' &+:,/«»³®`×', '----_\\""3R\'x')


class CarMake(models.Model):
    name = models.CharField(unique=True, max_length=127)
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


class CarModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(display=True)


class CarModel(models.Model):
    name = models.CharField(db_index=True, max_length=127)
    car_make = models.ForeignKey(CarMake)
    # old_id = models.IntegerField(unique=True, null=True)
    display = models.BooleanField(default=False)

    objects = models.Manager()
    objects_actual = CarModelManager()

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


class Generation(models.Model):
    name = models.CharField(max_length=127, blank=True)
    car_make = models.ForeignKey(CarMake)
    car_model = models.ForeignKey(CarModel)
    year_start = models.IntegerField()
    year_end = models.IntegerField(blank=True, null=True)
    display = models.BooleanField(default=False)

    class Meta:
        ordering = ['-year_start']
        unique_together = (('name', 'car_model', 'year_start', 'year_end'),)

    def __str__(self):
        return self.car_make.name + ' ' + self.car_model.name + ' ' + self.name + ' ' + str(self.year_start)

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
    def get_by_year(cls, car_model, year_start):
        try:
            return cls.objects.get(car_model=car_model, year_start=year_start)
        except MultipleObjectsReturned as e:
            print('MOR with {}, {}'.format(car_model, year_start))
            raise e
        except ObjectDoesNotExist as e:
            print('DNE with {}, {}'.format(car_model, year_start))
            raise e


def car_image_path(instance, filename):
    return 'car_images/{}/{}/{}/{}/{}'.format(instance.generation.car_make.name,
                                              instance.generation.car_model.name,
                                              instance.body.name,
                                              instance.generation.id,
                                              filename)


IMAGE_SIZES = {
    'm': (800, 800),
    's': (365, 365),
    'xs': (180, 180)
}


class Body(models.Model):
    name = models.CharField(unique=True, max_length=127)

    def __str__(self):
        return self.name

    @classmethod
    def get_by_name(cls, name):
        return cls.objects.get(name=name)

    @classmethod
    def get_by_name_loose(cls, name):
        # точку глотает кто ни попадя
        if name[-2:] == 'дв':
            try:
                return cls.objects.get(name__iexact=name+'.')
            except ObjectDoesNotExist:
                pass
        return cls.objects.get(name__iexact=name)


class CarImage(models.Model):
    generation = models.ForeignKey(Generation, db_index=True)
    body = models.ForeignKey(Body, db_index=True)
    image = models.ImageField(upload_to=car_image_path)
    main = models.BooleanField(default=False)

    def save(self, **kwargs):
        if self.image.name[:4] == 'main':
            self.main = True
        super().save(**kwargs)
        original_image = Image.open(self.image.file)
        original_path = self.image.path.rsplit('.', 1)
        for sz, dim in IMAGE_SIZES.items():
            resized_image = original_image.copy()
            resized_image.thumbnail(dim, Image.ANTIALIAS)
            resized_image.save(self.resized_path(original_path, sz))

    @staticmethod
    def resized_path(original_path, sz):
        return original_path[0] + '_' + sz + '.' + original_path[1]

    def __str__(self):
        # TODO добавить последний кусок урла
        return '{} ({})'.format(self.generation, self.body)


class Engine(models.Model):
    name = models.CharField(unique=True, max_length=127)

    def __str__(self):
        return self.name

    @classmethod
    def get_by_name(cls, name):
        return cls.objects.get(name=name)

    @classmethod
    def get_or_create_by_name(cls, name):
        return cls.objects.get_or_create(name=name)


class Gear(models.Model):
    name = models.CharField(unique=True, max_length=127)

    def __str__(self):
        return self.name

    @classmethod
    def get_by_name(cls, name):
        return cls.objects.get(name=name)


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
    name = models.CharField(unique=True, max_length=255)
    group = models.CharField(max_length=2, choices=GROUP_CHOICES)
    rank = models.SmallIntegerField()

    class Meta:
        unique_together = (('group', 'rank'),)

    def __str__(self):
        return "[" + self.group + "] " + self.name


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
    name = models.CharField(unique=True, max_length=255)
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

    def __str__(self):
        return ' '.join([str(self.generation), self.body.name, self.gear.name, self.engine.name, self.name])

    @property
    def safe_name(self):
        return self.name.replace('/', '%')

    def get_absolute_url(self):
        mod_params = {
            'car_make': self.car_make.name,
            'car_model': self.car_model.safe_name,
            # TODO эффективно ли это?
            'generation': self.generation.name if self.generation.name else '-',
            'body': self.body.name,
            'gear': self.gear.name,
            'engine': self.engine.name,
            'gen_year_start': self.generation.year_start,
            'complect': self.safe_name if self.safe_name else '-',
        }
        if self.cost is None:
            mod_params.update({'mod_id': self.id})
        else:
            mod_params.update({'cost': self.cost})
        url = reverse('kreddb:view_modification', kwargs=mod_params)
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


class SiteOptions(models.Model):
    option = models.CharField(max_length=127, unique=True)
    json_value = models.TextField()

    cache = dict()

    @classmethod
    def get_option(cls, option):
        if option in cls.cache:
            return cls.cache[option]
        else:
            return cls.load_option(option)

    @classmethod
    def load_option(cls, option):
        option_value = json.loads(cls.objects.values_list('json_value', flat=True).get(option=option))
        cls.cache[option] = option_value
        return option_value

    def set_option(self, option, value):
        self.option = option
        self.json_value = json.dumps(value)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.cache[self.option] = json.loads(self.json_value)
        super().save(force_insert, force_update, using, update_fields)
