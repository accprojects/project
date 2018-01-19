# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-12 11:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('all_files', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=128)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]
