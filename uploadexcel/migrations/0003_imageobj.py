# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-03-13 14:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploadexcel', '0002_table_color_fomat'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageObj',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='img/%y')),
            ],
        ),
    ]
