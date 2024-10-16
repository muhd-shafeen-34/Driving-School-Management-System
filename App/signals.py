# users/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Instructor, Student

@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'instructor':
            Instructor.objects.create(user=instance)  # Adjust as needed
        elif instance.role == 'student':
            Student.objects.create(user=instance)  # Adjust as needed
