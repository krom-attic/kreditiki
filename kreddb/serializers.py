from rest_framework import serializers

from kreddb.models import CarModel


class CarModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarModel

        fields = ('name',)
        read_only_fields = ('name',)
