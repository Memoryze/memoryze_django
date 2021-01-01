# Generated by Django 3.1.4 on 2020-12-23 09:17

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('played_recordings', django.contrib.postgres.fields.ArrayField(base_field=models.JSONField(null=True), default=list, size=None)),
                ('recently_played', django.contrib.postgres.fields.ArrayField(base_field=models.JSONField(null=True), default=list, size=None)),
            ],
        ),
        migrations.CreateModel(
            name='Audio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('recording', models.FileField(blank=True, null=True, upload_to='recordings/%Y/%m/%D/')),
                ('likes', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('categories', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=30), default=list, size=None)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/%Y/%m/%D/')),
            ],
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('audios', django.contrib.postgres.fields.ArrayField(base_field=models.JSONField(null=True), default=list, size=None)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
