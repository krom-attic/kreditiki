from csv import DictReader

from django.db import transaction

from kreddb.exceptions import CsvUploadException
from kreddb.models import Modification, Body, CarMake, Engine, Gear, Generation, CarModel


def _parse_row(row: dict) -> Modification:
    modification = Modification()
    modification.name = row['name']
    modification.cost = row['cost']
    try:
        modification.body = Body.get_by_name(row['body'])
    except Body.DoesNotExist:
        raise CsvUploadException("body")
    modification.car_make = CarMake.get_by_name(row['car_make'])
    modification.model_family = CarModel.get_first_for_model_family(modification.car_make, row['car_model']).model_family
    modification.engine = Engine.get_or_create_by_name(row['engine'])[0]
    modification.gear = Gear.get_by_name(row['gear'])
    modification.generation = Generation.get_by_year(modification.model_family, row['year_start'])
    modification.car_model = CarModel.get_by_main_parameters(row['car_model'], modification.generation, modification.body)
    return modification


def _save_parsed_modifications(modifications: list) -> None:
    for modification in modifications:
        modification.save()


@transaction.atomic()
def parse_csv(file):
    modifications = [_parse_row(row) for row in DictReader(file)]
    _save_parsed_modifications(modifications)
