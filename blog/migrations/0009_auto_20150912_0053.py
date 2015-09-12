# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import pystagram.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0008_post_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='photo',
            field=models.ImageField(null=True, upload_to='', validators=[pystagram.validators.jpeg_validator], blank=True),
        ),
    ]
