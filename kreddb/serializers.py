from rest_framework import serializers

from kreddb.models import ModelFamily


class CarModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = ModelFamily

        fields = ('name',)
        read_only_fields = ('name',)
