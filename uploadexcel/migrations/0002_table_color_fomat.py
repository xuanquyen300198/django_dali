# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-03-10 16:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploadexcel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='table_color_fomat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_hex', models.CharField(max_length=100)),
                ('code_dali', models.CharField(max_length=100)),
                ('number_img', models.IntegerField()),
            ],
        ),
    ]
