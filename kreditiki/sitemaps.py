from datetime import datetime

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from kreddb.models import CarMake, CarModel, Modification


class IndexSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8
    protocol = 'https'

    def items(self):
        return ['kreddb:list_car_makes']

    def lastmod(self, obj):
        return datetime.today().replace(day=28)

    def location(self, obj):
        return reverse(obj)


class CarMakeSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7
    protocol = 'https'

    def items(self):
        return CarMake.objects.filter(display=True)

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


class ModificationSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5
    limit = 100
    protocol = 'https'

    def items(self):
        return Modification.objects.filter(cost__gt=0)

    def lastmod(self, obj):
        return obj.updated_at
