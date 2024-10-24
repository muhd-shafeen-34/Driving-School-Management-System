from datetime import date
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')  # Superusers are admins by default
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role = models.CharField(max_length=10, choices=[('admin', 'Admin'), ('instructor', 'Instructor'), ('student', 'Student')])
    date_joined = models.DateTimeField(default=timezone.now)  # Add this field

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
class Instructor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    is_approved = models.BooleanField(default=False)
    dob = models.DateField(default=date(2000, 1, 1))

    def __str__(self):
        return self.name
    
class Package(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True, blank=True)# Many instructors can be assigned to a package
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField(help_text="Duration in days")
    
    def __str__(self):
        return self.name