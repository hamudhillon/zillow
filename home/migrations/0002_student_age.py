# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-03-16 04:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='age',
            field=models.IntegerField(default=None, max_length=5),
        ),
    ]
