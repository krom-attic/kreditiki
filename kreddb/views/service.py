from io import BytesIO
from io import StringIO

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic import View

from kreddb.bl.csv_export import generate_csv_template
from kreddb.bl.csv_import import parse_csv
from kreddb.bl.image_import import import_images
from kreddb.bl.site_options import save_promo_settings
from kreddb.models import SiteOptions


class UploadCarCsvView(LoginRequiredMixin, TemplateView):
    template_name = 'kreddb/service/upload_car_csv.html'

    def post(self, request, *args, **kwargs):
        file = request.FILES['csvfile']
        parse_csv(StringIO(file.read().decode()))
        return redirect('kreddb:service_upload_csv')


class DownloadCarCsvTemplate(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return generate_csv_template()


class UploadCarImagesView(LoginRequiredMixin, TemplateView):
    template_name = 'kreddb/service/upload_car_image.html'

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
        car_body = request.POST['car_body']
        if car_body == '':
            car_body = None
        import_images(BytesIO(file.read()), car_make_name, car_model_name, gen_start_year, car_body)
        return redirect('kreddb:service_upload_images')


class SetPromoView(LoginRequiredMixin, TemplateView):

    template_name = 'kreddb/service/set_promo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            promo_list = SiteOptions.get_option('promo')
        except ObjectDoesNotExist:
            promo_list = []
        for i in range(6 - len(promo_list)):
            promo_list.append(None)

        context['promo_list'] = promo_list
        return context

    def post(self, request, *args, **kwargs):
            promo_list = [(request.POST['gen_' + str(i)], request.POST['body_' + str(i)]) for i in range(6)]
            save_promo_settings(promo_list)
            return redirect('kreddb:service_set_promo')
