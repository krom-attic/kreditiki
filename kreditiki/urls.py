"""kreditiki URL Configuration
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap, index
from django.views.generic import TemplateView

from kreditiki import sitemaps as sm

# TODO sitemaps
sitemaps = {
    'index': sm.IndexSitemap,
    'car_make': sm.CarMakeSitemap,
    'car_model': sm.CarModelSitemap,
    'modifications': sm.ModificationSitemap
}

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    url(r'^sitemap\.xml$', index, {'sitemaps': sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^', include('kreddb.urls', namespace='kreddb'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    try:
        import debug_toolbar
        urlpatterns += [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ]
    except ImportError:
        pass  # не установлен и не надо

