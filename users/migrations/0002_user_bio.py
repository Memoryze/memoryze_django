# Generated by Django 3.1.4 on 2020-12-28 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.CharField(default='', max_length=300),
        ),
    ]
