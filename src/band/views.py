from rest_framework import viewsets

from . import serializers
from . import models

class BandViewSet(viewsets.ModelViewSet):
    queryset = models.Band.objects.all()
    serializer_class = serializers.BandSerializer