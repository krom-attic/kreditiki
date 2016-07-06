from io import StringIO

from django.views.generic import TemplateView
from django.views.generic.edit import BaseFormView

from kreddb.bl.csv_import import fake_parse_csv


class UploadCarCsvView(TemplateView):
    template_name = "kreddb/service/upload_car_csv.html"

    def post(self, request, *args, **kwargs):
        file = request.FILES['csvfile']
        fake_parse_csv(StringIO(file.read().decode()))
        return

