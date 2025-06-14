# Generated by Django 5.1.1 on 2024-10-30 10:32

import django.contrib.postgres.fields.ranges
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0010_rename_friday_time_classschedule_friday_end_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classschedule',
            name='friday_end',
        ),
        migrations.RemoveField(
            model_name='classschedule',
            name='friday_start',
        ),
        migrations.RemoveField(
            model_name='classschedule',
            name='monday_end',
        ),
        migrations.RemoveField(
            model_name='classschedule',
            name='monday_start',
        ),
        migrations.RemoveField(
            model_name='classschedule',
            name='saturday_end',
        ),
        migrations.RemoveField(
            model_name='classschedule',
            name='saturday_start',
        ),
        migrations.RemoveField(
            model_name='classschedule',
            name='thursday_end',
        ),
        migrations.RemoveField(
            model_name='classschedule',
            name='thursday_start',
        ),
        migrations.RemoveField(
            model_name='classschedule',
            name='tuesday_end',
        ),
        migrations.RemoveField(
            model_name='classschedule',
            name='tuesday_start',
        ),
        migrations.RemoveField(
            model_name='classschedule',
            name='wednesday_end',
        ),
        migrations.RemoveField(
            model_name='classschedule',
            name='wednesday_start',
        ),
        migrations.AddField(
            model_name='classschedule',
            name='friday_time_range',
            field=django.contrib.postgres.fields.ranges.DateTimeRangeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='classschedule',
            name='monday_time_range',
            field=django.contrib.postgres.fields.ranges.DateTimeRangeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='classschedule',
            name='saturday_time_range',
            field=django.contrib.postgres.fields.ranges.DateTimeRangeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='classschedule',
            name='thursday_time_range',
            field=django.contrib.postgres.fields.ranges.DateTimeRangeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='classschedule',
            name='tuesday_time_range',
            field=django.contrib.postgres.fields.ranges.DateTimeRangeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='classschedule',
            name='wednesday_time_range',
            field=django.contrib.postgres.fields.ranges.DateTimeRangeField(blank=True, null=True),
        ),
    ]
