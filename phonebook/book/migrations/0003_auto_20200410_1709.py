# Generated by Django 3.0.5 on 2020-04-10 17:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_auto_20200410_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phone',
            name='phone',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(999999999)]),
        ),
    ]
