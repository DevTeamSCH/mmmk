from django.db import models
from django.contrib.auth.models import User


class Band(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(User, related_name="bands")
    logourl = models.CharField(max_length=200, blank=True)
    contactemail = models.CharField(max_length=100, blank=True)
    website = models.CharField(blank=True, max_length=255)

    def is_member(self, user):
        return len(self.members.filter(id=user.id)) > 0

    def __str__(self):
        return self.name
