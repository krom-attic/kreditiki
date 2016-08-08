from csv import DictWriter

from django.http import HttpResponse

from kreddb.models import Equipment, Feature


def generate_csv_template():
        modification_fields = [
            'Название',
            'Стоимость',
            'Кузов',
            'Марка',
            'Модель',
            'Двигатель',
            'Коробка',
            'Название поколения',
            'Год поколения'
        ]

        equipment_fields = list(Equipment.objects.values_list('name', flat=True))

        feature_fields = list(Feature.objects.values_list('name', flat=True))

        fields = modification_fields + equipment_fields + feature_fields

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="template.csv"'

        # writer = DictWriter(response, fieldnames=fields)
        writer = DictWriter(response, fieldnames=modification_fields)
        writer.writeheader()

        return response
