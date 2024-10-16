# users/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Instructor, Student
from django.core.mail import send_mail
# @receiver(post_save, sender=CustomUser)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         if instance.role == 'instructor':
#             Instructor.objects.create(user=instance)  # Adjust as needed
#         elif instance.role == 'student':
#             Student.objects.create(user=instance)  # Adjust as needed



# @receiver(post_save, sender=CustomUser)
# def user_created_signal(sender, instance, created, **kwargs):
#     if created:
#         if instance.role == 'instructor':
#         # Action to perform when a new CustomUser is created
#             send_mail(
#                 'Welcome!',
#                 'Thanks for signing up!',
#                 'admin@drivingschool.com',
#                 [instance.email],
#                 fail_silently=False,
#             )