from datetime import datetime

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from kreddb.models import CarMake, CarModel, Modification


Sitemap.limit = 100


class IndexSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8

    def items(self):
        return [None]

    def lastmod(self, obj):
        return datetime.today().replace(day=28)

    def location(self, obj):
        return reverse('kreddb:list_car_makes')


class CarMakeSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return CarMake.objects.filter(display=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.filter_url()


class CarModelSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 1

    def items(self):
        return CarModel.objects.filter(display=True)

    def lastmod(self, obj):
        return obj.updated_at


class ModificationSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return Modification.objects.filter(cost__gt=0)

    def lastmod(self, obj):
        return obj.updated_at
