# Generated by Django 5.1.1 on 2024-10-27 05:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0005_student_instructor'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='package',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='App.package'),
        ),
    ]
