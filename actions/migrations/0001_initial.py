# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('verb', models.CharField(max_length=255, verbose_name='操作详情')),
                ('target_id', models.PositiveIntegerField(blank=True, db_index=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='执行时间')),
                ('target_ct', models.ForeignKey(blank=True, to='contenttypes.ContentType', related_name='target_obj', null=True)),
                ('user', models.ForeignKey(verbose_name='用户', related_name='actions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]
