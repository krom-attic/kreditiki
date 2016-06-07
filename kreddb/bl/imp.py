# import re
#
# from django.core.exceptions import ObjectDoesNotExist
#
# from kreddb.models import Mark, CarModelOld, GenerationOld, BodyOld, EngineOld, GearOld, ModificationOld,\
#     EquipmentLk, FeatureLk
# from kreddb.models import CarMake, CarModel, Generation, Body, Engine, Gear, Modification,\
#     EquipmentCost, Equipment, ModificationFeatures, Feature
#
#
# def get_old_car_makes():
#     available_makes = ModificationOld.objects.exclude(cost=None).values_list('mark', flat=True).distinct()
#     return Mark.objects.filter(id__in=available_makes)
#
#
# def import_car_makes(run_again=False):
#     if not run_again:
#         raise Exception('Уже запускалось!')
#     car_makes = get_old_car_makes()
#     print('Начинаю конвертацию марок')
#     for old in car_makes:
#         car_make = CarMake()
#         car_make.name = old.name
#         # car_make.old_id = old.id
#         car_make.save()
#     print('Закончил конвертацию марок')
#
#
# def get_old_car_models():
#     available_models = ModificationOld.objects.exclude(cost=None).values_list('car_model', flat=True).distinct()
#     return CarModelOld.objects.filter(id__in=available_models)
#
#
# def import_car_models(run_again=False):
#     if not run_again:
#         raise Exception('Уже запускалось!')
#     car_models = get_old_car_models()
#     print('Начинаю конвертацию моделей')
#     for old in car_models:
#         car_model = CarModel()
#         car_model.name = old.name
#         # car_model.car_make = CarMake.get_by_old_id(old.mark_id)
#         car_model.car_make = CarMake.get_by_name(old.mark.name)
#         # car_model.old_id = old.id
#         car_model.save()
#     print('Закончил конвертацию моделей')
#
#
# def get_old_generations():
#     available_gens = ModificationOld.objects.exclude(cost=None).values_list('generation', flat=True).distinct()
#     return GenerationOld.objects.filter(id__in=available_gens)
#
#
# def import_generations(run_again=False):
#     if not run_again:
#         raise Exception('Уже запускалось!')
#     generations = get_old_generations()
#     print('Начинаю конвертацию поколений')
#     for old in generations:
#         generation = Generation()
#         if old.generation is not None:
#             generation.name = old.generation
#         else:
#             generation.name = ''
#         # generation.car_make = CarMake.get_by_old_id(old.mark_id)
#         generation.car_make = CarMake.get_by_name(old.mark.name)
#         # generation.car_model = CarModel.get_by_old_id(old.car_model_id)
#         generation.car_model = CarModel.get_by_name(old.car_model.name, generation.car_make)
#         generation.year_start = old.top_age
#         generation.year_end = old.bottom_age
#         # generation.old_id = old.id
#         generation.save()
#     print('Закончил конвертацию поколений')
#
#
# def get_old_bodies():
#     available_bodies = ModificationOld.objects.exclude(cost=None).values_list('body', flat=True).distinct()
#     return BodyOld.objects.filter(id__in=available_bodies)
#
#
# def import_bodies(run_again=False):
#     if not run_again:
#         raise Exception('Уже запускалось!')
#     bodies = get_old_bodies()
#     print('Начинаю конвертацию корпусов')
#     for old in bodies:
#         body = Body()
#         body.name = old.name
#         # body.old_id = old.id
#         body.save()
#     print('Закончил конвертацию корпусов')
#
#
# def get_old_engines():
#     available_engines = ModificationOld.objects.exclude(cost=None).values_list('engine', flat=True).distinct()
#     return EngineOld.objects.filter(id__in=available_engines)
#
#
# def import_engines(run_again=False):
#     if not run_again:
#         raise Exception('Уже запускалось!')
#     print('Начинаю конвертацию двигателей')
#     for old in get_old_engines():
#         engine = Engine()
#         engine.name = old.name
#         # engine.old_id = old.id
#         engine.save()
#     print('Закончил конвертацию двигателей')
#
#
# def get_old_gears():
#     available_gears = ModificationOld.objects.exclude(cost=None).values_list('gear', flat=True).distinct()
#     return GearOld.objects.filter(id__in=available_gears)
#
#
# def import_gears(run_again=False):
#     if not run_again:
#         raise Exception('Уже запускалось!')
#     print('Начинаю конвертацию коробок')
#     for old in get_old_gears():
#         gear = Gear()
#         gear.name = old.name
#         # gear.old_id = old.id
#         gear.save()
#     print('Закончил конвертацию коробок')
#
#
# def get_old_modifications():
#     return ModificationOld.objects.exclude(cost=None)
#
#
# def import_modifications(run_again=False):
#     if not run_again:
#         raise Exception('Уже запускалось!')
#     print('Начинаю конвертацию комплектаций')
#     for old in get_old_modifications():
#         modification = Modification()
#         if old.equipment_name is not None:
#             modification.name = old.equipment_name
#         else:
#             modification.name = ''
#         # modification.car_make = CarMake.get_by_old_id(old.mark_id)
#         modification.car_make = CarMake.get_by_name(old.mark.name)
#         modification.car_model = CarModel.get_by_name(old.car_model.name, modification.car_make)
#         modification.generation = Generation.get_by_name_and_year(modification.car_model,
#                                                                      old.generation.top_age,
#                                                                      old.generation.bottom_age,
#                                                                      old.generation.generation or '')
#         modification.body = Body.get_by_name(old.body.name)
#         modification.gear = Gear.get_by_name(old.gear.name)
#         modification.engine = Engine.get_by_name(old.engine.name)
#         if old.cost != '':
#             modification.cost = old.cost
#         else:
#             modification.cost = None
#         modification.old_id = old.id
#         modification.save()
#     print('Закончил конвертацию комплектаций')
#
#
# def get_old_equipment():
#     return EquipmentLk.objects.all()
#
#
# def import_equipment(run_again=False):
#     if not run_again:
#         raise Exception('Уже запускалось!')
#     print('Начинаю конвертацию деталей комплектаций')
#     i = 0
#     RE_OPTION_PACKAGE = re.compile(r'.+:.+')
#     for old in get_old_equipment():
#         i += 1
#         # modification_car_make = CarMake.get_by_name(old_modification.mark.name)
#         # modification_car_model = CarModel.get_by_name(old_modification.car_model.name, modification_car_make)
#         # modification_generation = Generation.get_by_name_and_year(modification_car_model,
#         #                                                              old_modification.generation.top_age,
#         #                                                              old_modification.generation.bottom_age,
#         #                                                              old_modification.generation.generation or '')
#         # modification_body = Body.get_by_name(old_modification.body.name)
#         # modification_gear = Gear.get_by_name(old_modification.gear.name)
#         # modification_engine = Engine.get_by_name(old_modification.engine.name)
#         # if old_modification.cost != '':
#         #     modification_cost = old_modification.cost
#         # else:
#         #     modification_cost = None
#         # if old_modification.equipment_name is not None:
#         #     modification_name = old_modification.equipment_name
#         # else:
#         #     modification_name = ''
#         # equipment_cost.modification = Modification.get_by_params(modification_generation,
#         #                                                             modification_body,
#         #                                                             modification_gear,
#         #                                                             modification_engine,
#         #                                                             modification_cost,
#         #                                                             modification_name)
#         try:
#             modification = Modification.get_by_old_id(old.modification_id)
#         except ObjectDoesNotExist:
#             continue
#
#         name = old.equipment_dict.name
#         if RE_OPTION_PACKAGE.match(name):
#             # print('Пакет опций?\n{}'.format(name).encode('cp866', 'ignore').decode('cp866'))
#             continue
#
#         equipment, _ = Equipment.objects.get_or_create(name=name)
#
#         equipment_cost = EquipmentCost()
#         equipment_cost.modification = modification
#         equipment_cost.equipment = equipment
#         equipment_cost.cost = old.equipment_dict.cost
#         equipment_cost.save()
#
#         if i % 1000 == 0:
#             print(i)
#     print('Закончил конвертацию деталей комплектаций')
#
#
# def get_old_features():
#     return FeatureLk.objects.all()
#
#
# def import_features(run_again=False):
#     if not run_again:
#         raise Exception('Уже запускалось!')
#     print('Начинаю конвертацию характеристик')
#     i = 0
#     for old in get_old_features():
#         i += 1
#
#         try:
#             modification = Modification.get_by_old_id(old.modification_id)
#         except ObjectDoesNotExist:
#             continue
#
#         feature, _ = Feature.objects.get_or_create(name=old.feature_dict.name)
#
#         modification_feature = ModificationFeatures()
#         modification_feature.modification = modification
#         modification_feature.feature = feature
#         modification_feature.value = old.feature_dict.value
#         modification_feature.save()
#
#         if i % 1000 == 0:
#             print(i)
#     print('Закончил конвертацию характеристик')
#
#
# def imp():
#     print('Начинаю очистку')
#     CarMake.objects.all().delete()
#     CarModel.objects.all().delete()
#     Generation.objects.all().delete()
#     Body.objects.all().delete()
#     Engine.objects.all().delete()
#     Gear.objects.all().delete()
#     Modification.objects.all().delete()
#     EquipmentCost.objects.all().delete()
#     Equipment.objects.all().delete()
#     ModificationFeatures.objects.all().delete()
#     Feature.objects.all().delete()
#     print('Закончил очистку')
#     import_car_makes(True)
#     import_car_models(True)
#     import_generations(True)
#     import_bodies(True)
#     import_engines(True)
#     import_gears(True)
#     import_modifications(True)
#     import_equipment(True)
#     import_features(True)
