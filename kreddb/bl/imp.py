import re

from kreddb.models import Mark, CarModel, Generation, Body, Engine, Gear, Modification,\
    EquipmentLk
from kreddb.models import CarMake, CarModelNew, GenerationNew, BodyNew, EngineNew, GearNew, ModificationNew,\
    EquipmentCost, Equipment


def get_old_car_makes():
    return Mark.objects.all()


def import_car_makes(run_again=False):
    if not run_again:
        raise Exception('Уже запускалось!')
    car_makes = get_old_car_makes()
    print('Начинаю конвертацию марок')
    for old in car_makes:
        car_make = CarMake()
        car_make.name = old.name
        # car_make.old_id = old.id
        car_make.save()
    print('Закончил конвертацию марок')


def get_old_car_models():
    return CarModel.objects.all()


def import_car_models(run_again=False):
    if not run_again:
        raise Exception('Уже запускалось!')
    car_models = get_old_car_models()
    print('Начинаю конвертацию моделей')
    for old in car_models:
        car_model = CarModelNew()
        car_model.name = old.name
        # car_model.car_make = CarMake.get_by_old_id(old.mark_id)
        car_model.car_make = CarMake.get_by_name(old.mark.name)
        # car_model.old_id = old.id
        car_model.save()
    print('Закончил конвертацию моделей')


def get_old_generations():
    return Generation.objects.all()


def import_generations(run_again=False):
    if not run_again:
        raise Exception('Уже запускалось!')
    generations = get_old_generations()
    print('Начинаю конвертацию поколений')
    for old in generations:
        generation = GenerationNew()
        if old.generation is not None:
            generation.name = old.generation
        else:
            generation.name = ''
        # generation.car_make = CarMake.get_by_old_id(old.mark_id)
        generation.car_make = CarMake.get_by_name(old.mark.name)
        # generation.car_model = CarModelNew.get_by_old_id(old.car_model_id)
        generation.car_model = CarModelNew.get_by_name(old.car_model.name, generation.car_make)
        generation.year_start = old.top_age
        generation.year_end = old.bottom_age
        # generation.old_id = old.id
        generation.save()
    print('Закончил конвертацию поколений')


def get_old_bodies():
    return Body.objects.all()


def import_bodies(run_again=False):
    if not run_again:
        raise Exception('Уже запускалось!')
    bodies = get_old_bodies()
    print('Начинаю конвертацию корпусов')
    for old in bodies:
        body = BodyNew()
        body.name = old.name
        # body.old_id = old.id
        body.save()
    print('Закончил конвертацию корпусов')


def get_old_engines():
    return Engine.objects.all()


def import_engines(run_again=False):
    if not run_again:
        raise Exception('Уже запускалось!')
    print('Начинаю конвертацию двигателей')
    for old in get_old_engines():
        engine = EngineNew()
        engine.name = old.name
        # engine.old_id = old.id
        engine.save()
    print('Закончил конвертацию двигателей')


def get_old_gears():
    return Gear.objects.all()


def import_gears(run_again=False):
    if not run_again:
        raise Exception('Уже запускалось!')
    print('Начинаю конвертацию коробок')
    for old in get_old_gears():
        gear = GearNew()
        gear.name = old.name
        # gear.old_id = old.id
        gear.save()
    print('Закончил конвертацию коробок')


def get_old_modifications():
    return Modification.objects.all()


def import_modifications(run_again=False):
    if not run_again:
        raise Exception('Уже запускалось!')
    print('Начинаю конвертацию комплектаций')
    for old in get_old_modifications():
        modification = ModificationNew()
        if old.equipment_name is not None:
            modification.name = old.equipment_name
        else:
            modification.name = ''
        # modification.car_make = CarMake.get_by_old_id(old.mark_id)
        modification.car_make = CarMake.get_by_name(old.mark.name)
        modification.car_model = CarModelNew.get_by_name(old.car_model.name, modification.car_make)
        modification.generation = GenerationNew.get_by_name_and_year(modification.car_model,
                                                                     old.generation.top_age,
                                                                     old.generation.bottom_age,
                                                                     old.generation.generation or '')
        modification.body = BodyNew.get_by_name(old.body.name)
        modification.gear = GearNew.get_by_name(old.gear.name)
        modification.engine = EngineNew.get_by_name(old.engine.name)
        if old.cost != '':
            modification.cost = old.cost
        else:
            modification.cost = None
        modification.old_id = old.id
        modification.save()
    print('Закончил конвертацию комплектаций')


def get_old_equipment():
    return EquipmentLk.objects.all()


def import_equipment(run_again=False):
    if not run_again:
        raise Exception('Уже запускалось!')
    print('Начинаю конвертацию деталей комплектаций')
    i = 0
    RE_OPTION_PACKAGE = re.compile(r'.+:.+(,.+)+')
    for old in get_old_equipment():
        i += 1
        # modification_car_make = CarMake.get_by_name(old_modification.mark.name)
        # modification_car_model = CarModelNew.get_by_name(old_modification.car_model.name, modification_car_make)
        # modification_generation = GenerationNew.get_by_name_and_year(modification_car_model,
        #                                                              old_modification.generation.top_age,
        #                                                              old_modification.generation.bottom_age,
        #                                                              old_modification.generation.generation or '')
        # modification_body = BodyNew.get_by_name(old_modification.body.name)
        # modification_gear = GearNew.get_by_name(old_modification.gear.name)
        # modification_engine = EngineNew.get_by_name(old_modification.engine.name)
        # if old_modification.cost != '':
        #     modification_cost = old_modification.cost
        # else:
        #     modification_cost = None
        # if old_modification.equipment_name is not None:
        #     modification_name = old_modification.equipment_name
        # else:
        #     modification_name = ''
        # equipment_cost.modification = ModificationNew.get_by_params(modification_generation,
        #                                                             modification_body,
        #                                                             modification_gear,
        #                                                             modification_engine,
        #                                                             modification_cost,
        #                                                             modification_name)
        name = old.equipment_dict.name
        if RE_OPTION_PACKAGE.match(name):
            print('Пакет опций?\n{}'.format(name))
            continue

        equipment, _ = Equipment.objects.get_or_create(name=name)

        equipment_cost = EquipmentCost()
        equipment_cost.modification = ModificationNew.get_by_old_id(old.modification_id)
        equipment_cost.equipment = equipment
        equipment_cost.cost = old.equipment_dict.cost
        equipment_cost.save()

        if i % 1000 == 0:
            print(i)
    print('Закончил конвертацию деталей комплектаций')


def imp():
    print('Начинаю очистку')
    # CarMake.objects.all().delete()
    # CarModelNew.objects.all().delete()
    # GenerationNew.objects.all().delete()
    # BodyNew.objects.all().delete()
    # EngineNew.objects.all().delete()
    # GearNew.objects.all().delete()
    ModificationNew.objects.all().delete()
    EquipmentCost.objects.all().delete()
    Equipment.objects.all().delete()
    print('Закончил очистку')
    # import_car_makes(True)
    # import_car_models(True)
    # import_generations(True)
    # import_bodies(True)
    # import_engines(True)
    # import_gears(True)
    import_modifications(True)
    import_equipment(True)
