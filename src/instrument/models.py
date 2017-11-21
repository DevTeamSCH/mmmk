from django.db import models
from django.contrib.auth.models import User


class Instrument(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, related_name='instruments', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
