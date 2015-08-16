from django.conf.urls import url

from kreddb import views

# TODO: в gear и engine * заменить на +. Тогда можно будет поменять местами регэкспы для DetailView и ListView
# TODO чего уж точно не должно быть в урлах, так это прямых слешей
URL_RE_PARTS = {
    'mark': r'(?P<mark>[\w \-\(\)]+)',
    'model': r'(?P<model>[\w \.\-\(\)\'\&\,\+\!\xc2\xbb\xc2\xab\:]+)',
    'generation': r'(?P<generation>[\w\d \-\(\)\,\/\+]*)',
    'gen_year_start': r'(?P<gen_year_start>\d{4})',
    'gen_year_end': r'(?P<gen_year_end>\d{4})',
    'body': r'(?P<body>[\w\d \.\,\-\(\)\+\xc2\xb3\\\'\"]+)',
    'engine': r'(?P<engine>[\w \.\-\(\)\xd7]*)',
    'gear': r'(?P<gear>[\w \-\(\)]*)',
    'modification': r'(?P<modification>[\w\d \.\-\(\)\/\+\xc2\xbb\xc2\xab\&\"\,\xc2\xae\`]*)',
    'cost': r'(?P<cost>\d+)',
    'mod_id': r'(?P<mod_id>\d+)'
}

urlpatterns = [
    url(r'^c/$', views.MarkListView.as_view(), name='list_marks'),
    url(r'^c/{mark}/$'.format(**URL_RE_PARTS), views.ModelListView.as_view(), name='list_models'),
    url(r'^c/{mark}/{model}/$'.format(**URL_RE_PARTS), views.ModificationListView.as_view(), name='list_modifications'),
    # url(r'c/^(?P<mark>[\w \-\(\)]+)/(?P<model>[\w \-\(\)\']+)/$', views.GenerationListView.as_view(), name='list_generations'),
    # url(r'c/^(?P<mark>[\w \-\(\)]+)/(?P<model>[\w \-\(\)\']+)/(?P<generation>[\w \-\(\)]+)/(?P<body>[\w \-\(\)]+)/'
    #     r'(?P<engine>[\w \.\-\(\)\xd7]+)/(?P<gear>[\w \-\(\)]+)/$', views.ModificationListView.as_view(), name='list_modifications'),
    # url(r'^c/(?P<mark>[\w \-\(\)]+)/(?P<model>[\w \-\(\)\']+)/(?P<generation>[\w \-\(\)]+)/(?P<body>[\w \-\(\)]+)/'
    #     r'(?P<engine>[\w \.\-\(\)\xd7]+)/(?P<gear>[\w \-\(\)]+)/(?P<modification>[\w \.\-\(\)]+)$',
    #     views.ModificationDetailView.as_view(), name='view_modification')
    # url(r'^c/(?P<mark>[\w \-\(\)]+)/(?P<model>[\w \-\(\)\']+)/(?P<generation>[\w \-\(\)]+)/(?P<body>[\w \.\-\(\)]+)/'
    #     r'(?P<engine>[\w \.\-\(\)\xd7]+)/(?P<gear>[\w \-\(\)]+)/(?P<modification>[\w \.\-\(\)]+)$',
    #     views.ModificationDetailView.as_view(), name='view_modification')
    url(r'^[cс]/{mark}/{model}/{gen_year_start}-{gen_year_end}/{generation}/{modification}/{body}/{engine}/{gear}/в '
        r'кредит за {cost}/$'.format(**URL_RE_PARTS), views.ModificationDetailView.as_view(), name='view_modification'),
    url(r'^[cс]/{mark}/{model}/{gen_year_start}-{gen_year_end}/{generation}/{modification}/{body}/{engine}/{gear}/в '
        r'кредит/{mod_id}$'.format(**URL_RE_PARTS), views.ModificationDetailView.as_view(), name='view_modification'),
    url(r'^[cс]/{mark}/{model}/{gen_year_start}-{gen_year_end}/{generation}/{modification}/{body}/{engine}/{gear}/'
        r'$'.format(**URL_RE_PARTS), views.ModificationListView.as_view(), name='list_modifications'),
    # "c" поддерживается на обоих языках
]
