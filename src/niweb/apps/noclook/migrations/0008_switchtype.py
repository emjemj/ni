# -*- coding: utf-8 -*-
# Generated by Django 1.11.25 on 2019-11-21 15:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('noclook', '0007_auto_20190320_1254'),
    ]

    operations = [
        migrations.CreateModel(
            name='SwitchType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('ports', models.CharField(blank=True, help_text=b'Autogenerate ports. "," separator. ex: Et1,Et2,Et3 alt ge-0/0/0,ge-0/0/1', max_length=1024)),
            ],
        ),
    ]