# Generated by Django 3.0.3 on 2020-04-10 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dc_parse', '0002_auto_20200410_2241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediavkphoto',
            name='photo',
            field=models.IntegerField(unique=True),
        ),
    ]