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
            name='BusinessAccount',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('legalbusinessname', models.CharField(max_length=200, unique=True)),
                ('businesslogo', models.ImageField(upload_to='')),
                ('address_line1', models.CharField(max_length=100)),
                ('address_line2', models.CharField(max_length=100, null=True, blank=True)),
                ('city', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True, blank=True)),
                ('state', models.CharField(max_length=100)),
                ('zipcode', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('phone', models.CharField(max_length=100)),
                ('websiteurl', models.CharField(max_length=100, null=True, blank=True)),
                ('active', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('accountuser', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BusinessCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='BusinessLocations',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('locationname', models.CharField(max_length=100, unique=True)),
                ('address_line1', models.CharField(max_length=100)),
                ('address_line2', models.CharField(max_length=100, null=True, blank=True)),
                ('gps', models.CharField(max_length=100, null=True, blank=True)),
                ('city', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True, blank=True)),
                ('state', models.CharField(max_length=100)),
                ('zipcode', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
                ('websiteurl', models.CharField(max_length=100, null=True, blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('business', models.ForeignKey(to='businesses.BusinessAccount')),
            ],
        ),
        migrations.CreateModel(
            name='BusinessRating',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('review', models.CharField(max_length=500)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('businessId', models.ForeignKey(to='businesses.BusinessLocations')),
                ('userId', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='businessaccount',
            name='businesscategory',
            field=models.ForeignKey(to='businesses.BusinessCategory'),
        ),
        migrations.AlterUniqueTogether(
            name='businessaccount',
            unique_together=set([('accountuser', 'legalbusinessname')]),
        ),
    ]
