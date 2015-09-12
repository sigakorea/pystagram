# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_photograph'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='langlat',
            field=models.CharField(max_length=100, blank=True, null=True),
        ),
    ]
