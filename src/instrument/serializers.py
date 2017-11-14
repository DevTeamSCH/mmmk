from rest_framework import serializers
from django.contrib.auth.models import User

from . import models


class InstrumentSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.Instrument
            fields = '__all__'