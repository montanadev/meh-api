# Generated by Django 4.2 on 2023-04-10 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IotCommand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acked', models.BooleanField()),
                ('sensor', models.TextField()),
            ],
        ),
    ]
