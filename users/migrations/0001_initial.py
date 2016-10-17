# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('businesses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Points',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField(default=0)),
                ('businessLocation', models.ForeignKey(to='businesses.BusinessLocations')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Preferences',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('businesslocationid', models.ForeignKey(to='businesses.BusinessLocations', null=True, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ReferralRewards',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('redeemed', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('businessLocation', models.ForeignKey(to='businesses.BusinessLocations')),
                ('referredto', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='referredto')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('redeemed', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('businessLocation', models.ForeignKey(to='businesses.BusinessLocations')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='referralrewards',
            unique_together=set([('user', 'businessLocation', 'referredto')]),
        ),
        migrations.AlterUniqueTogether(
            name='preferences',
            unique_together=set([('user', 'businesslocationid')]),
        ),
        migrations.AlterUniqueTogether(
            name='points',
            unique_together=set([('user', 'businessLocation')]),
        ),
    ]
