# Generated by Django 3.1.6 on 2021-02-16 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='code',
            field=models.CharField(default='0FlpX0', max_length=30),
        ),
    ]