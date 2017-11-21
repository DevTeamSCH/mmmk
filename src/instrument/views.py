from rest_framework import viewsets

from . import serializers

from . import models

class InstrumentViewSet(viewsets.ModelViewSet):
    queryset = models.Instrument.objects.all()
    serializer_class = serializers.InstrumentSerializer
