# Generated by Django 3.0.3 on 2020-04-18 19:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dc_main', '0004_auto_20200301_2359'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='tag_name',
            new_name='name',
        ),
    ]