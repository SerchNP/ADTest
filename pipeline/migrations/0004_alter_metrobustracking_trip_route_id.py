# Generated by Django 3.2.7 on 2021-10-04 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pipeline', '0003_rename_geographical_point_metrobustracking_geographic_point'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metrobustracking',
            name='trip_route_id',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]
