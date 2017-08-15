from django.db import models
from django.contrib.auth.models import User


class Page(models.Model):
    name = models.CharField(max_length=255)
    visible = models.BooleanField(default=False)


class Entry(models.Model):
    page = models.ForeignKey(Page, related_name='entries', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    content = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
