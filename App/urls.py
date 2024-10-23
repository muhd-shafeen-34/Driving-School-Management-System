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
    path('admin_home',Admin_Views.admin_dashboard,name='admin_home'),
    path('add_staff',Admin_Views.add_staff,name='add_staff'),
    path('add_package',Admin_Views.add_package,name='add_package'),
    path('add_staff_save',Admin_Views.add_staff_save,name='add_staff_save'),
    path('add_package_save',Admin_Views.add_package_save,name='add_package_save'),
    path('manage_staff',Admin_Views.manage_staff,name='manage_staff'),
    path('manage_package',Admin_Views.manage_package,name='manage_package'),
    path('edit_staff/<str:staff_id>',Admin_Views.edit_staff,name='edit_staff'),
    path('edit_staff_save',Admin_Views.edit_staff_save,name='edit_staff_save'),
    path('staff_home',Staff_Views.staff_dashboard,name='staff_home'),
    path('student_home',Student_Views.student_dashboard,name='student_home'),
    path('logout/', views.custom_logout, name='logout'),
    
]
