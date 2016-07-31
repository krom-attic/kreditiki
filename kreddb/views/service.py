from io import BytesIO
from io import StringIO

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from kreddb.bl.csv_import import fake_parse_csv
from kreddb.bl.image_import import import_images


class UploadCarCsvView(LoginRequiredMixin, TemplateView):
    template_name = "kreddb/service/upload_car_csv.html"

    def post(self, request, *args, **kwargs):
        file = request.FILES['csvfile']
        fake_parse_csv(StringIO(file.read().decode()))
        return


class UploadCarImagesView(LoginRequiredMixin, TemplateView):
    template_name = "kreddb/service/upload_car_image.html"

    def post(self, request, *args, **kwargs):
        file = request.FILES['zipfile']
        car_make_name = request.POST['car_make']
        if car_make_name == '':
            car_make_name = None
        car_model_name = request.POST['car_model']
        if car_model_name == '':
            car_model_name = None
        gen_start_year = request.POST['car_gen_start']
        if gen_start_year == '':
            gen_start_year = None
        import_images(BytesIO(file.read()), car_make_name, car_model_name, gen_start_year)
        return redirect('kreddb:service_upload_images')
