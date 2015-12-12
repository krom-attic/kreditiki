from django.conf.urls import include, url

from rest_framework_nested import routers

from kreddb import views

router = routers.SimpleRouter()
router.register(r'car_models', views.CarModelViewSet)

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
    'gen_year_end': r'(?P<gen_year_end>\d{4})',
    'body': r'(?P<body>[\w\d \.\,\-\(\)\+\xc2\xb3\\\'\"]+)',
    # 'body': r'(?P<body>[\w\d\.\-\(\)\\\'\"]+)',
    'engine': r'(?P<engine>[\w \.\-\(\)\xd7]*)',
    # 'engine': r'(?P<engine>[\w\.\-\(\)]*)',
    'gear': r'(?P<gear>[\w\-\(\)]*)',
    'complect': r'(?P<complect>[\w\d \.\-\(\)\+\xc2\xbb\xc2\xab\&\"\,\xc2\xae\`%]*)',
    # 'complect': r'(?P<complect>[\w\d\.\-\(\)\"\']*)',
    'cost': r'(?P<cost>\d+)',
    'mod_id': r'(?P<mod_id>\d+)'
}

urlpatterns = [
    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/carmodels/{car_make}/?$'.format(**URL_RE_PARTS), views.CarModelListAPIView.as_view(), name='test_list'),
    url(r'^api/v1/modifications/{car_make}/{car_model}/?$'.format(**URL_RE_PARTS), views.ListModificationsAPIView.as_view(), name='test_list'),

    url(r'^/?$', views.MarkListView.as_view(), name='list_marks'),
    # "c" поддерживается на обоих языках
    url(r'^[cс]/$', views.MarkListView.as_view(), name='list_marks'),
    url(r'^[cс]/selector/$', views.CarSelectorDispatchView.as_view(), name="carselector"),
    url(r'^[cс]/{car_make}/(?P<all>все/)?$'.format(**URL_RE_PARTS), views.CarModelListView.as_view(), name='list_car_models'),
    url(r'^[cс]/{car_make}/{car_model}/(?P<all>все/)?$'.format(**URL_RE_PARTS), views.ModificationListView.as_view(),
        name='list_modifications'),
    url(r'^[cс]/{car_make}/{car_model}/{gen_year_start}-{gen_year_end}/{generation}/{complect}/{body}/{engine}/{gear}/'
        r'в кредит за {cost}/$'.format(**URL_RE_PARTS), views.ModificationDetailView.as_view(),
        name='view_modification'),
    # url(r'c/^(?P<car_make>[\w \-\(\)]+)/(?P<car_model>[\w \-\(\)\']+)/$', views.GenerationListView.as_view(), name='list_generations'),
    # url(r'c/^(?P<car_make>[\w \-\(\)]+)/(?P<car_model>[\w \-\(\)\']+)/(?P<generation>[\w \-\(\)]+)/(?P<body>[\w \-\(\)]+)/'
    #     r'(?P<engine>[\w \.\-\(\)\xd7]+)/(?P<gear>[\w \-\(\)]+)/$', views.ModificationListView.as_view(), name='list_modifications'),
    # url(r'^c/(?P<car_make>[\w \-\(\)]+)/(?P<car_model>[\w \-\(\)\']+)/(?P<generation>[\w \-\(\)]+)/(?P<body>[\w \-\(\)]+)/'
    #     r'(?P<engine>[\w \.\-\(\)\xd7]+)/(?P<gear>[\w \-\(\)]+)/(?P<complect>[\w \.\-\(\)]+)$',
    #     views.ModificationDetailView.as_view(), name='view_modification')
    # url(r'^c/(?P<car_make>[\w \-\(\)]+)/(?P<car_model>[\w \-\(\)\']+)/(?P<generation>[\w \-\(\)]+)/(?P<body>[\w \.\-\(\)]+)/'
    #     r'(?P<engine>[\w \.\-\(\)\xd7]+)/(?P<gear>[\w \-\(\)]+)/(?P<complect>[\w \.\-\(\)]+)$',
    #     views.ModificationDetailView.as_view(), name='view_modification')
    url(r'^[cс]/{car_make}/{car_model}/{gen_year_start}-{gen_year_end}/{generation}/{complect}/{body}/{engine}/{gear}/'
        r'в кредит/{mod_id}$'.format(**URL_RE_PARTS), views.ModificationDetailView.as_view(), name='view_modification'),
    url(r'^[cс]/{car_make}/{car_model}/{gen_year_start}-{gen_year_end}/{generation}/{complect}/{body}/{engine}/{gear}/'
        r'(?P<all>all)?/$'.format(**URL_RE_PARTS), views.ModificationListView.as_view(), name='list_modifications'),
    # url(r'^ajax/car-models', views.ListCarModelsAjaxView.as_view(), name='ajax_list_car_models'),
    url(r'^ajax/modifications', views.ListModificationsAjaxView.as_view(), name='ajax_list_modifications'),
    url(r'^ajax/modification-search', views.SearchModificationsAjaxView.as_view(), name='ajax_list_modifications'),
]
