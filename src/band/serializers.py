from rest_framework import serializers

from . import models


class BandSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Band
        fields = ('url', 'name', 'description', 'members', 'logourl', 'contactemail', 'website')
