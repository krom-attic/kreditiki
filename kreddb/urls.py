from django.conf.urls import url

from kreddb import views

# TODO: в gear и engine * заменить на +. Тогда можно будет поменять местами регэкспы для DetailView и ListView
URL_RE_PARTS = {
    # 'mark': r'(?P<mark>[\w \-\(\)]+)',
    'mark': r'(?P<mark>[\w\-\(\)]+)',
    # 'car_model': r'(?P<car_model>[\w \.\-\(\)\'\&\,\+\!\xc2\xbb\xc2\xab\:]+)',
    'car_model': r'(?P<car_model>[\w\.\-\(\)\'\,\!\"\\]+)',
    # 'generation': r'(?P<generation>[\w\d \-\(\)\,\/\+]*)',
    'generation': r'(?P<generation>[\w\d\-\(\)\,]*)',
    'gen_year_start': r'(?P<gen_year_start>\d{4})',
    'gen_year_end': r'(?P<gen_year_end>\d{4})',
    # 'body': r'(?P<body>[\w\d \.\,\-\(\)\+\xc2\xb3\\\'\"]+)',
    'body': r'(?P<body>[\w\d\.\-\(\)\\\'\"]+)',
    # 'engine': r'(?P<engine>[\w \.\-\(\)\xd7]*)',
    'engine': r'(?P<engine>[\w\.\-\(\)]*)',
    'gear': r'(?P<gear>[\w\-\(\)]*)',
    # 'modification': r'(?P<modification>[\w\d \.\-\(\)\/\+\xc2\xbb\xc2\xab\&\"\,\xc2\xae\`]*)',
    'modification': r'(?P<modification>[\w\d\.\-\(\)\"\']*)',
    'cost': r'(?P<cost>\d+)',
    'mod_id': r'(?P<mod_id>\d+)'
}

urlpatterns = [
    url(r'^/?$', views.MarkListView.as_view(), name='list_marks'),
    url(r'^c/$', views.MarkListView.as_view(), name='list_marks'),
    url(r'^c/{mark}/(all)?/$'.format(**URL_RE_PARTS), views.CarModelListView.as_view(), name='list_car_models'),
    url(r'^c/{mark}/{car_model}/(?P<all>все/)?$'.format(**URL_RE_PARTS), views.ModificationListView.as_view(),
        name='list_modifications'),
    # url(r'c/^(?P<mark>[\w \-\(\)]+)/(?P<car_model>[\w \-\(\)\']+)/$', views.GenerationListView.as_view(), name='list_generations'),
    # url(r'c/^(?P<mark>[\w \-\(\)]+)/(?P<car_model>[\w \-\(\)\']+)/(?P<generation>[\w \-\(\)]+)/(?P<body>[\w \-\(\)]+)/'
    #     r'(?P<engine>[\w \.\-\(\)\xd7]+)/(?P<gear>[\w \-\(\)]+)/$', views.ModificationListView.as_view(), name='list_modifications'),
    # url(r'^c/(?P<mark>[\w \-\(\)]+)/(?P<car_model>[\w \-\(\)\']+)/(?P<generation>[\w \-\(\)]+)/(?P<body>[\w \-\(\)]+)/'
    #     r'(?P<engine>[\w \.\-\(\)\xd7]+)/(?P<gear>[\w \-\(\)]+)/(?P<modification>[\w \.\-\(\)]+)$',
    #     views.ModificationDetailView.as_view(), name='view_modification')
    # url(r'^c/(?P<mark>[\w \-\(\)]+)/(?P<car_model>[\w \-\(\)\']+)/(?P<generation>[\w \-\(\)]+)/(?P<body>[\w \.\-\(\)]+)/'
    #     r'(?P<engine>[\w \.\-\(\)\xd7]+)/(?P<gear>[\w \-\(\)]+)/(?P<modification>[\w \.\-\(\)]+)$',
    #     views.ModificationDetailView.as_view(), name='view_modification')
    url(r'^[cс]/{mark}/{car_model}/{gen_year_start}-{gen_year_end}/{generation}/{modification}/{body}/{engine}/{gear}/'
        r'в кредит за {cost}/$'.format(**URL_RE_PARTS), views.ModificationDetailView.as_view(),
        name='view_modification'),
    url(r'^[cс]/{mark}/{car_model}/{gen_year_start}-{gen_year_end}/{generation}/{modification}/{body}/{engine}/{gear}/'
        r'в кредит/{mod_id}$'.format(**URL_RE_PARTS), views.ModificationDetailView.as_view(), name='view_modification'),
    url(r'^[cс]/{mark}/{car_model}/{gen_year_start}-{gen_year_end}/{generation}/{modification}/{body}/{engine}/{gear}/'
        r'(?P<all>all)?/$'.format(**URL_RE_PARTS), views.ModificationListView.as_view(), name='list_modifications'),
    # "c" поддерживается на обоих языках
    url(r'^ajax/car-models', views.ListCarModelsAjaxView.as_view(), name='ajax_list_car_models'),
    url(r'^ajax/modifications', views.ListModificationsAjaxView.as_view(), name='ajax_list_modifications'),
    url(r'^ajax/modification-search', views.SearchModificationsAjaxView.as_view(), name='ajax_list_modifications'),
]
