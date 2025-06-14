"""
URL configuration for DSM project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from App import Admin_Views, Staff_Views, Student_Views, views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('',views.index),
    path('login',views.custom_login_view, name='login'),
    path('register',views.student_register, name='register'),
    path('save_student',views.save_student, name='save_student'),
    path('admin_home',Admin_Views.admin_dashboard,name='admin_home'),
    path('add_staff',Admin_Views.add_staff,name='add_staff'),
    path('add_package',Admin_Views.add_package,name='add_package'),
    path('students_under/<int:package_id>',Admin_Views.students_under_this_package,name='students_under'),
    path('edit_package/<str:package_id>',Admin_Views.edit_package,name='edit_package'),
    path('edit_package_save',Admin_Views.edit_package_save,name='edit_package_save'),
    
    path('add_staff_save',Admin_Views.add_staff_save,name='add_staff_save'),
    path('add_package_save',Admin_Views.add_package_save,name='add_package_save'),
    path('assign_staff_package/<int:package_id>',Admin_Views.assign_staff_package,name='assign_staff_package'),
    
    
    path('assign_this_instructor/<int:package_id>/<int:staff_id>',Admin_Views.assign_this_instructor,name='assign_this_instructor'),
    
    path('manage_staff',Admin_Views.manage_staff,name='manage_staff'),
    path('manage_package',Admin_Views.manage_package,name='manage_package'),
    path('edit_staff/<str:staff_id>',Admin_Views.edit_staff,name='edit_staff'),
    path('delete_staff/<str:staff_id>',Admin_Views.delete_staff,name="delete_Staff"),
    path('edit_staff_save',Admin_Views.edit_staff_save,name='edit_staff_save'),
    path('view_student_feedback',Admin_Views.student_feedback_message,name="view_student_feedback"),
    path('view_staff_feedback',Admin_Views.instructor_feedback_message,name="view_staff_feedback"),
    path('staff_home',Staff_Views.staff_dashboard,name='staff_home'),
    path('logout', views.custom_logout, name='logout'),
    
    
    # student
    path('pending_student',Admin_Views.pending_student,name="pending_student"),
    path('manage_student',Admin_Views.manage_student,name="manage_student"),
    path('approve_student/<int:student_id>',Admin_Views.approve_student,name="approve_student"),
    path('reject_student/<int:student_id>',Admin_Views.reject_student,name="reject_student"),
    path('delete_student/<int:student_id>',Admin_Views.delete_student,name="delete_student"),
    path('edit_student/<int:student_id>',Admin_Views.edit_student,name="edit_student"),
    path('edit_student_save',Admin_Views.edit_student_save,name='edit_student_save'),
    path('waiting_page',views.waiting_page,name="waiting_page"),
    path('assign_staff_student/<int:student_id>',Admin_Views.assign_staff_student,name='assign_staff_student'),
    path('assign_this_instructor_to_student/<int:student_id>/<int:staff_id>',Admin_Views.assign_this_instructor_to_student,name='assign_this_instructor_to_student'),
    
    
    #instructor
    path('instructor_profile',Staff_Views.instructor_profile,name="instructor_profile"),
    path('students_under_instructor',Staff_Views.students_under_instructor,name="students_under_instructor"),
    path('edit_profile_instructor/<int:staff_id>',Staff_Views.edit_profile_instructor,name="edit_profile_instructor"),
    path('save_instructor_profile',Staff_Views.save_instructor_profile,name="save_instructor_profile"),
    path('assign_class_timings/<int:staff_id>/<int:student_id>',Staff_Views.assign_class_schedule_form,name='assign_class _timings'),
    path('save_class_schedule',Staff_Views.save_class_schedule,name="save_class_schedule"),
    path('instructor_sent_feedback',Staff_Views.staff_feedback,name="staff_sent_feedback"),
    
    #students
    path('student_home',Student_Views.student_dashboard,name='student_home'),
    path('student_profile',Student_Views.student_profile,name='student_profile'),
    path('edit_student_profile/<int:student_id>',Student_Views.student_edit_profile,name="edit_student_profile"),
    path('save_student_profile',Student_Views.save_student_profile,name='save_student_profile'),
    path('student_instructor',Student_Views.student_instructor,name="student_instructor"),
    path('student_sent_feedback',Student_Views.student_feedback,name="student_feedback"),
]
