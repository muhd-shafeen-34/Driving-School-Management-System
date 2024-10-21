# users/signals.py
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Instructor, CustomUser
# @receiver(post_save, sender=CustomUser)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         if instance.role == 'instructor':
#             Instructor.objects.create(user=instance)  # Adjust as needed
#         elif instance.role == 'student':
#             Student.objects.create(user=instance)  # Adjust as needed





# @receiver(post_save, sender=Instructor)
# def send_instructor_email(sender, instance, created, **kwargs):
#     if created:
#         # Prepare email details
#         fullname = instance.name
#         email = instance.user.email  # Get email from the related CustomUser
#         password = instance.user.password  # You should store the password securely

#         subject = "Welcome to the Driving School"
#         message = f"""
#         Hello {fullname},

#         You have been successfully added as an instructor to our Driving School Management System.

#         Your login credentials are:
#         - Email: {email}
#         - Password: {password}

#         Please log in at [Login URL] and consider changing your password after the first login.

#         Best regards,
#         Admin Team
#         """

#         # Send the email
#         send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)


# Import your models


# Send email with raw password



def send_welcome_email(Instructor, raw_password):
    fullname = Instructor.name
    email = Instructor.user.email

    # Prepare the email content
    subject = "Welcome to the Driving School"
    message = f"""
    Hello {fullname},

    You have been successfully added as an instructor to our Driving School Management System.

    Your login credentials are:
    - Email: {email}
    - Password: {raw_password}


    Best regards,
    Admin Team
    """

    # Send the email
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)