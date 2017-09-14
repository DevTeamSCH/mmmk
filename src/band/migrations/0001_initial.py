# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-15 20:18
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Band',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('logourl', models.CharField(blank=True, max_length=200)),
                ('contactemail', models.CharField(blank=True, max_length=100)),
                ('website', models.CharField(blank=True, max_length=255)),
                ('members', models.ManyToManyField(related_name='bands', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]