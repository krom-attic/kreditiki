import json
import os
from random import randint

from PIL import Image
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Min, Count

from kreddb.bl.calculator import calculate_best_interest_and_credit
from kreddb.url_utils.cipher import cipher_id

POSITIONS = (('T', 'Наверху'), ('B', 'Внизу'))


class EnhancedManager(models.Manager):
    def random(self):
        count = self.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        return self.all()[random_index]


class CarMakeManager(EnhancedManager):
    def get_queryset(self):
        return super().get_queryset().filter(display=True)


class CarMake(models.Model):
    name = models.CharField(unique=True, max_length=127)
    display = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    objects_actual = CarMakeManager()

    class Meta:
        ordering = ['name']

    # TODO при сохранении нужно проверять отсутствие "запрещённых" символов типа "_"

    def __str__(self):
        return self.name

    @property
    def safe_name(self):
        return self.name.replace(' ', '_')

    def get_absolute_url(self):
        return reverse('kreddb:list_model_families', kwargs=dict(
            car_make=self.safe_name
        ))

    def filter_url(self):
        return reverse('kreddb:list_model_families', kwargs={'car_make': self.safe_name})

    @classmethod
    def get_by_name(cls, name):
        return cls.objects_actual.get(name=name)

    @classmethod
    def get_by_safe_name(cls, safe_name: str):
        name = safe_name.replace('_', ' ')
        return cls.get_by_name(name)

    @classmethod
    def get_displayed(cls):
        return cls.objects_actual.all()

    @classmethod
    def get_random_carmake(cls):
        return cls.objects_actual.random()


class ModelFamily(models.Model):
    # на данный момент лукапа из урла нет, но если понадобится, стоит учесть, что здесь могут быть пробелы и слэши
    name = models.CharField(db_index=True, max_length=127)
    car_make = models.ForeignKey(CarMake)
    display = models.BooleanField(default=False)

    def __str__(self):
        return self.car_make.name + ' ' + self.name

    @property
    def safe_name(self):
        return self.name.replace('/', '\\').replace(' ', '_')


class Generation(models.Model):
    name = models.CharField(max_length=127, blank=True)
    car_make = models.ForeignKey(CarMake)
    model_family = models.ForeignKey(ModelFamily)
    year_start = models.IntegerField()
    year_end = models.IntegerField(blank=True, null=True)
    display = models.BooleanField(default=False)

    class Meta:
        ordering = ['-year_start']
        unique_together = (('name', 'model_family', 'year_start', 'year_end'),)

    def __str__(self):
        return self.car_make.name + ' ' + self.model_family.name + ' ' + self.name + ' ' + str(self.year_start)

    @property
    def safe_name(self):
        return self.name.replace('/', '\\').replace(' ', '_')

    @property
    def url_kwargs(self):
        url_kwargs = {'car_make': self.car_make.safe_name, 'model_family': self.model_family.safe_name,
                      'name': self.safe_name,
                      'body': '-', 'engine': '-', 'gear': '-'}
        return url_kwargs

    # TODO не должен использоваться
    def get_absolute_url(self):
        return reverse('kreddb:list_modifications', kwargs=self.url_kwargs)

    @classmethod
    def get_for_model(cls, car_make, model_family, year_start):
        return cls.objects.get(car_make=car_make, model_family=model_family, year_start=year_start)

    @classmethod
    def get_by_year(cls, model_family, year_start):
        try:
            return cls.objects.get(model_family=model_family, year_start=year_start)
        except MultipleObjectsReturned as e:
            # TODO Change to logging
            print('MOR with {}, {}'.format(model_family, year_start))
            raise e
        except ObjectDoesNotExist as e:
            print('DNE with {}, {}'.format(model_family, year_start))
            raise e

    @classmethod
    def get_latest(cls, model_family):
        return cls.objects.filter(model_family=model_family).order_by('-year_start').first()


class Body(models.Model):
    name = models.CharField(unique=True, max_length=127)

    def __str__(self):
        return self.name

    @property
    def safe_name(self):
        return self.name.replace(' ', '_')

    @classmethod
    def get_by_name(cls, name):
        return cls.objects.get(name=name)

    @classmethod
    def get_by_name_loose(cls, name):
        # точку глотает кто ни попадя
        if name[-2:] == 'дв':
            try:
                return cls.objects.get(name__iexact=name + '.')
            except ObjectDoesNotExist:
                pass
        return cls.objects.get(name__iexact=name)


class CarModelManager(EnhancedManager):
    def get_queryset(self):
        return super().get_queryset().filter(display=True)


class CarModel(models.Model):
    # TODO сделать, чтобы заполнялось автоматически из семейства, если пустое при сохранении
    name = models.CharField(max_length=127)
    model_family = models.ForeignKey(ModelFamily, db_index=True)
    generation = models.ForeignKey(Generation, db_index=True)
    body = models.ForeignKey(Body, db_index=True)
    display = models.BooleanField(default=False)
    related = models.ManyToManyField('self', blank=True)
    price_per_day = models.PositiveIntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    objects_actual = CarModelManager()

    class Meta:
        unique_together = (('name', 'generation', 'body'),)

    def __str__(self):
        return ' '.join([str(self.model_family), str(self.generation), self.name, str(self.body)])

    @property
    def model_name(self):
        return ' '.join([
            self.name,
            self.body.name,
        ])

    @property
    def safe_name(self):
        return self.name.replace('/', '\\').replace(' ', '_')

    @classmethod
    def get_by_id(cls, id):
        return cls.objects_actual.get(pk=id)

    @classmethod
    def get_by_name(cls, name, generation: Generation, body: Body):
        return cls.objects_actual.get(name=name, generation=generation, body=body)

    @classmethod
    def get_by_main_parameters(cls, name, generation, body):
        return cls.objects_actual.get(name_iexact=name, generation=generation, body=body)

    @classmethod
    def get_first_for_model_family(cls, car_make: CarMake, name: str):
        return cls.objects_actual.filter(model_family__car_make=car_make, name__iexact=name).first()

    def get_absolute_url(self):
        return reverse('kreddb:list_modifications', kwargs=dict(
            car_make=self.model_family.car_make.safe_name,
            car_model=self.safe_name,
            gen_year_start=self.generation.year_start,
            body=self.body.safe_name,
            object_id=cipher_id(str(self.id)),
        ))

    def update_price(self):
        cost = self.modification_set.aggregate(Min('cost'))['cost__min']
        if cost is not None:
            self.price_per_day = calculate_best_interest_and_credit(cost)
        else:
            # TODO залогировать
            self.price_per_day = None
        self.save()
        return self.price_per_day

    def get_price_per_day(self):
        if self.price_per_day is None:
            return self.update_price()
        else:
            return self.price_per_day

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        try:
            if not self.model_family:
                self.model_family = self.generation.model_family
        except ModelFamily.DoesNotExist:
            self.model_family = self.generation.model_family
        self.model_family.car_make.save()
        super().save(force_insert, force_update, using, update_fields)

    @classmethod
    def get_random_carmodel(cls):
        return cls.objects_actual.random()


class CarDescription(models.Model):
    car_model = models.ForeignKey(CarModel, db_index=True)
    description = models.TextField()
    description_pos = models.CharField(max_length=1, choices=POSITIONS)

    class Meta:
        unique_together = (('car_model', 'description_pos'),)

    @classmethod
    def get_by_model(cls, car_model: CarModel):
        return {description['description_pos']: description.get('description') for description in
                cls.objects.filter(car_model=car_model).values('description', 'description_pos')}


def car_image_path(instance, filename):
    return 'car_images/{}/{}/{}/{}/{}'.format(instance.car_model.model_family.car_make.name,
                                              instance.car_model.name,
                                              instance.car_model.body.name,
                                              instance.car_model.generation.id,
                                              filename)


IMAGE_SIZES = {
    'm': (800, 800),
    's': (365, 365),
    'xs': (180, 180)
}


class CarImage(models.Model):
    generation = models.ForeignKey(Generation, db_index=True, null=True)
    body = models.ForeignKey(Body, db_index=True, null=True)
    image = models.ImageField(upload_to=car_image_path)
    main = models.BooleanField(default=False)
    car_model = models.ForeignKey(CarModel)

    def save(self, **kwargs):
        original_image = Image.open(self.image.file)
        if os.path.basename(self.image.name)[:4] == 'main':
            self.main = True
        super().save(**kwargs)
        original_path = self.image.path.rsplit('.', 1)
        for sz, dim in IMAGE_SIZES.items():
            resized_image = original_image.copy()
            resized_image.thumbnail(dim, Image.ANTIALIAS)
            resized_image.save(self.resized_path(original_path, sz))

    @staticmethod
    def resized_path(original_path, sz):
        return original_path[0] + '_' + sz + '.' + original_path[1]

    @classmethod
    def get_main_car_image(cls, car_model: CarModel):
        return cls.objects.get(car_model=car_model, main=True).image

    def __str__(self):
        return '{} ({})'.format(self.car_model, self.image.path.rsplit(os.sep, 1)[1])


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
    # TODO удалить следующие четыре поля? это же дублирование!
    car_make = models.ForeignKey(CarMake)
    model_family = models.ForeignKey(ModelFamily, db_index=True)
    generation = models.ForeignKey(Generation)
    body = models.ForeignKey(Body)

    car_model = models.ForeignKey(CarModel, db_index=True, null=True)
    gear = models.ForeignKey(Gear)
    engine = models.ForeignKey(Engine)
    cost = models.IntegerField(blank=True, null=True)
    equipment = models.ManyToManyField(Equipment, through='EquipmentCost')
    features = models.ManyToManyField(Feature, through='ModificationFeatures')
    old_id = models.IntegerField(unique=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return ' '.join([str(self.generation), self.body.name, self.gear.name, self.engine.name, self.name])

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # TODO не отображть избыточные поля при редактировании модели
        self.body = self.car_model.body
        self.generation = self.car_model.generation
        self.model_family = self.generation.model_family
        self.car_make = self.model_family.car_make
        self.car_model.update_price()
        self.car_model.save()
        super().save(force_insert, force_update, using, update_fields)

    @property
    def safe_name(self):
        return self.name.replace('/', '\\').replace(' ', '_')

    @property
    def modification_name(self):
        return ' '.join((self.name, self.body.name, self.engine.name, self.gear.name))

    def get_absolute_url(self):
        mod_params = {
            'car_make': self.car_make.safe_name,
            'car_model': self.car_model.safe_name,
            # TODO эффективно ли это?
            'generation': self.generation.safe_name if self.generation.safe_name else '-',
            'body': self.body.safe_name,
            'gear': self.gear.name,
            'engine': self.engine.name,
            'gen_year_start': self.generation.year_start,
            'complect': self.safe_name if self.safe_name else '-',
            'object_id': cipher_id(str(self.id))
        }
        url = reverse('kreddb:view_modification', kwargs=mod_params)
        return url

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
    def get_by_car_model(cls, car_model: CarModel):
        return cls.objects.filter(car_model=car_model).order_by('cost')


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
        if self.id is None:
            try:
                self.id = SiteOptions.objects.values_list('id', flat=True).get(option=self.option)
            except SiteOptions.DoesNotExist:
                pass  # сохраним новый элемент без ID
        super().save(force_insert, force_update, using, update_fields)
