from rest_framework import serializers

from . import models


class InstrumentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Instrument
        fields = ('url', 'name', 'type', 'description', 'user')
