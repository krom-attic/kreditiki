from django.conf.urls import url

from kreddb import views

# TODO: в gear и engine * заменить на +. Тогда можно будет поменять местами регэкспы для DetailView и ListView
URL_RE_PARTS = {
    'mark': r'(?P<mark>[\w \-\(\)]+)',
    'model': r'(?P<model>[\w \.\-\(\)\'\&\,\+\!\xc2\xbb\xc2\xab\:]+)',
    'generation': r'(?P<generation>[\w\d \-\(\)\,\/\+]*)',
    'body': r'(?P<body>[\w\d \.\,\-\(\)\+\xc2\xb3\\\'\"]+)',
    'engine': r'(?P<engine>[\w \.\-\(\)\xd7]*)',
    'gear': r'(?P<gear>[\w \-\(\)]*)',
    'modification': r'(?P<modification>[\w\d \.\-\(\)\/\+\xc2\xbb\xc2\xab\&\"\,\xc2\xae\`]*)',
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
    url(r'^c/{mark}/{model}/{generation}/{modification}/{body}/{engine}/{gear}/'
        r'хочу/$'.format(**URL_RE_PARTS),
        views.ModificationDetailView.as_view(), name='view_modification'),
    url(r'^c/{mark}/{model}/{generation}/{modification}/{body}/{engine}/{gear}/$'.format(**URL_RE_PARTS),
        views.ModificationListView.as_view(), name='list_modifications'),
    # идея: возможно "c" должна поддерживаться на обоих языках
]
