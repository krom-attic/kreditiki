from django.conf.urls import url

from kreddb.views import views, service

# TODO: в gear и engine * заменить на +. Тогда можно будет поменять местами регэкспы для DetailView и ListView
# TODO: жаваскрипт-то в апи всё равно говносимволы использует!
URL_RE_PARTS = {
    'car_make': r'(?P<car_make>[\w \-\(\)]+)',
    # 'mark': r'(?P<mark>[\w\-\(\)]+)',
    'car_model': r'(?P<car_model>[\w \.\-\(\)\'\&\,\+\!\xc2\xbb\xc2\xab\:%]+)',
    # 'car_model': r'(?P<car_model>[\w\.\-\(\)\'\,\!\"\\ ]+)',
    'generation': r'(?P<generation>[\w\d \-\(\)\,\+]*)',
    # 'generation': r'(?P<generation>[\w\d\-\(\)\,]*)',
    'gen_year_start': r'(?P<gen_year_start>\d{4})',
    # 'gen_year_end': r'(?P<gen_year_end>\d{4})',
    'body': r'(?P<body>[\w\d \.\,\-\(\)\+\xc2\xb3\\\'\"]+)',
    # 'body': r'(?P<body>[\w\d\.\-\(\)\\\'\"]+)',
    'engine': r'(?P<engine>[\w \.\-\(\)\+\xd7]*)',
    # 'engine': r'(?P<engine>[\w\.\-\(\)]*)',
    'gear': r'(?P<gear>[\w\-\(\)]*)',
    'complect': r'(?P<complect>[\w\d \.\-\(\)\+\xc2\xbb\xc2\xab\&\"\,\xc2\xae\`%]*)',
    # 'complect': r'(?P<complect>[\w\d\.\-\(\)\"\']*)',
    'cost': r'(?P<cost>\d+)',
    'object_id': r'(?P<object_id>[_zQxJkVbPyG]+)'
}

urlpatterns = [
    # TODO что это?
    url(r'^api/car_makes/{car_make}/car_models/$'.format(**URL_RE_PARTS),
        views.CarModelListAPIView.as_view(),
        name='api_list_car_models'),
    # TODO что это?
    url(r'^api/modification/{object_id}/data/$'.format(**URL_RE_PARTS),
        views.ModificationDataApiView.as_view(),
        name='modification_data'),

    # TODO заменить credit на кредит
    url(r'^$', views.CarMakeListView.as_view(), name='list_marks'),
    url(r'^кредит/$', views.CarMakeListView.as_view(), name='list_marks'),

    url(r'^selector/$', views.CarSelectorDispatchView.as_view(), name="carselector"),

    url(r'^кредит/{car_make}/(?P<all>все/)?$'.format(**URL_RE_PARTS), views.CarModelListView.as_view(), name='list_model_families'),

    url(r'^кредит/{car_make}/{car_model}/{body}/{gen_year_start}/{object_id}/(?P<all>все/)?$'.format(**URL_RE_PARTS),
        views.ModificationListView.as_view(), name='list_modifications'),

    # TODO можно после gen_year_start передавать ещё несколько годов через запятую
    url(r'^кредит/{car_make}/{car_model}/{body}/{gen_year_start}/{generation}/{complect}/{engine}/{gear}/'
        r'{object_id}/$'.format(**URL_RE_PARTS), views.ModificationDetailView.as_view(),
        name='view_modification'),
    url(r'^кредит/{car_make}/{car_model}/{body}/{gen_year_start}/{generation}/{complect}/{engine}/{gear}/'
        r'{object_id}$'.format(**URL_RE_PARTS), views.ModificationDetailView.as_view(), name='view_modification'),

    url(r'^кредит/заявка/', views.CreditApplicationView.as_view(), name='credit_application'),

    url(r'^service/upload_csv/$', service.UploadCarCsvView.as_view(), name='service_upload_csv'),
    url(r'^service/csv_template/$', service.DownloadCarCsvTemplate.as_view(), name='service_download_csv_template'),
    url(r'^service/upload_images/$', service.UploadCarImagesView.as_view(), name='service_upload_images'),
    url(r'^service/set_promo/$', service.SetPromoView.as_view(), name='service_set_promo'),
]
