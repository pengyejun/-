# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-10-21 21:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0005_auto_20171020_1637'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='teacher_img',
            field=models.ImageField(blank=True, null=True, upload_to='org_teather/%Y/%m', verbose_name='photo'),
        ),
    ]