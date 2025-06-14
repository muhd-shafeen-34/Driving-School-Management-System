# Generated by Django 5.1.1 on 2024-10-29 18:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0007_instructor_age_instructor_license_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('monday_time', models.TimeField(blank=True, null=True)),
                ('tuesday_time', models.TimeField(blank=True, null=True)),
                ('wednesday_time', models.TimeField(blank=True, null=True)),
                ('thursday_time', models.TimeField(blank=True, null=True)),
                ('friday_time', models.TimeField(blank=True, null=True)),
                ('saturday_time', models.TimeField(blank=True, null=True)),
                ('sunday_time', models.TimeField(blank=True, null=True)),
                ('instructor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='instructor_schedules', to='App.instructor')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student_schedules', to='App.student')),
            ],
        ),
    ]
