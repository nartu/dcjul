# Generated by Django 3.0.3 on 2020-04-10 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dc_parse', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediavkphoto',
            name='post',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
