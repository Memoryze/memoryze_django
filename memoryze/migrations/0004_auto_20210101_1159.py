# Generated by Django 3.1.4 on 2021-01-01 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memoryze', '0003_auto_20201223_0920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audio',
            name='image',
            field=models.ImageField(null=True, upload_to='images/%Y/%m/%D/'),
        ),
    ]
