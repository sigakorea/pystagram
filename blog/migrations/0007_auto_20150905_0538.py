# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_post_langlat'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='langlat',
            new_name='lnglat',
        ),
    ]
