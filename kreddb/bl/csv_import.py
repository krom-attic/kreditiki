from csv import DictReader

from django.core.exceptions import ObjectDoesNotExist

from kreddb.models import Modification, Body, CarMake, CarModel, Engine, Gear, Generation


def _parse_row(row: dict) -> Modification:
    # TODO нужно начинать транзакцию
    modification = Modification()
    modification.name = row['name']
    modification.cost = row['cost']
    modification.body = Body.get_by_name(row['body'])
    modification.car_make = CarMake.get_by_name(row['car_make'])
    modification.car_model = CarModel.get_by_name(row['car_model'], modification.car_make)
    modification.engine = Engine.get_or_create_by_name(row['engine'])
    modification.gear = Gear.get_by_name(row['gear'])
    try:
        modification.generation = Generation.get_by_year(modification.car_model,
                                                         row['year_start'])
    except ObjectDoesNotExist:
        pass  # TODO нужно создавать руками
    return modification


def _save_parsed_modifications(modifications: list) -> None:
    for _ in modifications:
        pass


def fake_parse_csv(file):
    modifications = [_parse_row(row) for row in DictReader(file)]
    _save_parsed_modifications(modifications)
