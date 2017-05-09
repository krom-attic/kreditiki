from datetime import datetime, timedelta

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from kreddb.models import CarMake, CarModel


class IndexSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8
    protocol = 'https'

    def items(self):
        return ['kreddb:list_car_makes']

    def lastmod(self, obj):
        return datetime.today().replace(day=28) - timedelta(days=31)

    def location(self, obj):
        return reverse(obj)


class CarMakeSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7
    protocol = 'https'

    def items(self):
        return CarMake.get_displayed()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.filter_url()


class CarModelSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 1
    limit = 100
    protocol = 'https'

    def items(self):
        return CarModel.objects.filter(display=True)

    def lastmod(self, obj):
        return obj.updated_at
