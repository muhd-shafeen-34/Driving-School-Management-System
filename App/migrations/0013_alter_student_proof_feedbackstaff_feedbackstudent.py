# Generated by Django 5.1.1 on 2024-10-31 17:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0012_student_profile_picture_student_proof'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='proof',
            field=models.FileField(blank=True, null=True, upload_to='students/ID_Proofs/'),
        ),
        migrations.CreateModel(
            name='FeedbackStaff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.TextField()),
                ('reply', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('staff', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='App.instructor')),
            ],
        ),
        migrations.CreateModel(
            name='FeedbackStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.TextField()),
                ('reply', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='App.student')),
            ],
        ),
    ]
