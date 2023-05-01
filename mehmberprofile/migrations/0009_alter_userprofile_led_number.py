# Generated by Django 4.2 on 2023-05-01 11:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mehmberprofile', '0008_alter_userprofile_led_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='led_number',
            field=models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MaxValueValidator(2000), django.core.validators.MinValueValidator(0)], verbose_name='LED Number'),
        ),
    ]
