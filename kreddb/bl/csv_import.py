from csv import DictReader

from django.db import transaction

from kreddb.models import Modification, Body, CarMake, ModelFamily, Engine, Gear, Generation, CarModel


def _parse_row(row: dict) -> Modification:
    modification = Modification()
    modification.name = row['name']
    modification.cost = row['cost']
    modification.body = Body.get_by_name(row['body'])
    modification.car_make = CarMake.get_by_name(row['car_make'])
    # TODO вынести этот код в модель
    modification.model_family = CarModel.objects.filter(
        model_family__car_make=modification.car_make, name__iexact=row['car_model']
    ).first().model_family
    modification.engine = Engine.get_or_create_by_name(row['engine'])[0]
    modification.gear = Gear.get_by_name(row['gear'])
    modification.generation = Generation.get_by_year(modification.model_family, row['year_start'])
    # TODO вынести этот код в модель
    modification.car_model = CarModel.objects.get(
        name__iexact=row['car_model'],
        generation=modification.generation,
        body=modification.body
    )
    return modification


def _save_parsed_modifications(modifications: list) -> None:
    for modification in modifications:
        modification.save()


@transaction.atomic()
def parse_csv(file):
    modifications = [_parse_row(row) for row in DictReader(file)]
    _save_parsed_modifications(modifications)
