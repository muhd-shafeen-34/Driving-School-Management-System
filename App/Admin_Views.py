from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from App import models
from django.contrib import messages

@never_cache
@login_required(login_url='login')
def admin_dashboard(req):
    if req.user.role == 'admin':
        return render(req, 'App/Admin/admin_dashboard.html')
#     elif req.user.role=='instructor':
#         return rednder(req, 'App/Staff/staff_dashboard.html')
    else:
        return HttpResponseForbidden("you do not have permission to this page")

def add_staff(req):
    return render(req, 'App/Admin/add_staff_template.html')

def add_staff_save(req):
    if req.method != 'POST':
        return HttpResponse("adding staff is failed")
    else:
        fullname = req.POST.get('full_name')
        email = req.POST.get('email')
        password = req.POST.get('password')
        specialization = req.POST.get('specialization')
        phone = req.POST.get('phone_number')
        try:
            user = models.CustomUser.objects.create_user(email=email,password=password,role="instructor")
            Instructor = models.Instructor.objects.create(user=user, name=fullname, specialization=specialization, phone=phone)
            user.save()
            Instructor.save()
            messages.success(req,"Successfully added staff")
            return HttpResponseRedirect('add_staff')
        except:
            return HttpResponseRedirect('add_staff')
        
         
        