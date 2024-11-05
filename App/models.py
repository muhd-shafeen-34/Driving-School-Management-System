from datetime import date
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import DateTimeRangeField
from psycopg2.extras import DateTimeTZRange  # Needed to set time ranges

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
    age = models.TextField(max_length=100,default="18")
    profile_picture = models.ImageField(upload_to='instructors/profile_pics/', blank=True, null=True)  # For image upload
    specialization = models.CharField(max_length=255)
    license = models.FileField(upload_to='instructors/licenses/', blank=True, null=True)  # For image upload
    phone = models.CharField(max_length=20)

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
    
    
class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True, blank=True)# Many instructor can be assigned to a student
    package = models.ForeignKey(Package,on_delete=models.SET_NULL,null=True, blank=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    profile_picture = models.ImageField(upload_to='students/profile_pics/', blank=True, null=True)  # For image upload
    proof = models.FileField(upload_to='students/ID_Proofs/', blank=True, null=True)  # For image upload
    is_approved = models.BooleanField(default=False)
    dob = models.DateField(default=date(2000, 1, 1))

    def __str__(self):
        return self.name
    
    

class ClassSchedule(models.Model):
    instructor = models.ForeignKey('Instructor', on_delete=models.CASCADE, null=True, related_name='instructor_schedules')
    student = models.ForeignKey('Student', on_delete=models.CASCADE, null=True, related_name='student_schedules')
    start_date = models.DateField()
    end_date = models.DateField()

    # Using DateTimeRangeField for time ranges
    monday_time_range = DateTimeRangeField(null=True, blank=True)
    tuesday_time_range = DateTimeRangeField(null=True, blank=True)
    wednesday_time_range = DateTimeRangeField(null=True, blank=True)
    thursday_time_range = DateTimeRangeField(null=True, blank=True)
    friday_time_range = DateTimeRangeField(null=True, blank=True)
    saturday_time_range = DateTimeRangeField(null=True, blank=True)
    

    def __str__(self):
        return f"{self.student} - {self.instructor} from {self.start_date} to {self.end_date}"


class FeedbackStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE,null=True)
    feedback = models.TextField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedbackStaff(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE,null=True)
    feedback = models.TextField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    