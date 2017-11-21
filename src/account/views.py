from django.contrib.auth.models import User

from rest_framework import viewsets

from . import serializers

class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.AccountSerializer
