# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(verbose_name='作者', related_name='blog_posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='body',
            field=models.TextField(verbose_name='文章内容'),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_time',
            field=models.DateTimeField(verbose_name='创建日期', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='publish_time',
            field=models.DateTimeField(verbose_name='发布日期', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='post',
            name='recommend',
            field=models.BooleanField(verbose_name='推荐博文', default=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(verbose_name='文章短标签', unique_for_date='publish', max_length=250),
        ),
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('drate', 'Drate'), ('published', 'Published')], verbose_name='状态', default='drate', max_length=10),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(verbose_name='文章标题', max_length=250),
        ),
        migrations.AlterField(
            model_name='post',
            name='updated_time',
            field=models.DateTimeField(verbose_name='修改日期', auto_now=True),
        ),
    ]
