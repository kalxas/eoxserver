# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-02-06 15:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_service_visibility_cardinality_uniqueness'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicevisibility',
            name='service',
            field=models.CharField(choices=[('wms', 'WMS'), ('wcs', 'WCS'), ('os', 'OpenSearch'), ('wc', 'WebClient')], max_length=4),
        ),
    ]