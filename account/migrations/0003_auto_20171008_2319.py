# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-08 17:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20171007_1806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskuser',
            name='role',
            field=models.IntegerField(choices=[(3, 'student'), (1, 'admin'), (2, 'teacher')], default=3),
        ),
    ]