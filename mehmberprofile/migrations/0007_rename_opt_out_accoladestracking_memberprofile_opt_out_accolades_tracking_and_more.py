# Generated by Django 4.2 on 2023-04-10 04:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mehmberprofile', '0006_remove_memberprofile_hackerspace_rgb_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='memberprofile',
            old_name='opt_out_accoladestracking',
            new_name='opt_out_accolades_tracking',
        ),
        migrations.RenameField(
            model_name='memberprofile',
            old_name='opt_out_doorapptracking',
            new_name='opt_out_doorapp_tracking',
        ),
        migrations.RenameField(
            model_name='memberprofile',
            old_name='opt_out_ledwall',
            new_name='opt_out_led_wall',
        ),
        migrations.RenameField(
            model_name='memberprofile',
            old_name='opt_out_socialbot',
            new_name='opt_out_social_bot',
        ),
    ]
