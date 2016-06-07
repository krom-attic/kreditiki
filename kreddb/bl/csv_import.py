from csv import DictReader

from kreddb.models import Modification, Body, CarMake, CarModel, Engine, Gear, Generation


def _parse_row(row: dict) -> Modification:
    modification = Modification()
    modification.name = row['name']
    modification.cost = row['cost']
    modification.body = Body.get_by_name(row['body'])
    modification.car_make = CarMake.get_by_name(row['car_make'])
    modification.car_model = CarModel.get_by_name(row['car_model'], modification.car_make)
    modification.engine = Engine.get_by_name(row['engine'])
    modification.gear = Gear.get_by_name(row['gear'])
    modification.generation = Generation.get_by_name_and_year(modification.car_model,
                                                              row['year_start'],
                                                              row['year_end'],
                                                              row['generation'])
    return modification


def _save_parsed_modifications(modifications: list) -> None:
    for _ in modifications:
        pass


def fake_parse_csv(file):
    modifications = [_parse_row(row) for row in DictReader(file)]
    _save_parsed_modifications(modifications)
