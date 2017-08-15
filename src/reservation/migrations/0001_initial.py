# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-15 20:18
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        ('band', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DummyModelForGlobalPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False)),
                ('start', models.DateField()),
                ('end', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_conditional', models.BooleanField(default=False)),
                ('day_num', models.IntegerField(validators=[django.core.validators.MaxValueValidator(6), django.core.validators.MinValueValidator(0)])),
                ('hour_num', models.IntegerField(validators=[django.core.validators.MaxValueValidator(23), django.core.validators.MinValueValidator(0)])),
                ('unique_message', models.CharField(max_length=255, null=True)),
                ('allower', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_reservations', to=settings.AUTH_USER_MODEL)),
                ('band', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='band.Band')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RoomMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='StaticReservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.IntegerField()),
                ('time', models.TimeField()),
                ('band', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='static_reservations', to='band.Band')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='static_reservations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Week',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False)),
                ('number', models.IntegerField()),
                ('period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weeks', to='reservation.Period')),
            ],
        ),
        migrations.CreateModel(
            name='GlobalPermission',
            fields=[
            ],
            options={
                'verbose_name': 'global_permission',
                'proxy': True,
                'indexes': [],
            },
            bases=('auth.permission',),
        ),
        migrations.AddField(
            model_name='roommessage',
            name='week',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='reservation.Week'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='week',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='reservation.Week'),
        ),
    ]
