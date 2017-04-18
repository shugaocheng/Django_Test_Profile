# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('date_of_birth', models.DateTimeField(blank=True, verbose_name='时间', null=True)),
                ('photo', models.ImageField(blank=True, upload_to='users/%Y/%m/%d', verbose_name='图片')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
        ),
    ]
