# Generated by Django 5.1.1 on 2024-10-26 10:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0004_remove_student_age_student_dob'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='instructor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='App.instructor'),
        ),
    ]
