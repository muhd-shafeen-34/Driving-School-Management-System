from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from App import models
from App.signals import send_welcome_email
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
        raw_password = req.POST.get('password')
        specialization = req.POST.get('specialization')
        phone = req.POST.get('phone_number')
        try:
            user = models.CustomUser.objects.create_user(email=email,password=raw_password,role="instructor")
            Instructor = models.Instructor.objects.create(user=user, name=fullname, specialization=specialization, phone=phone)
            user.save()
            Instructor.save()
            send_welcome_email(Instructor, raw_password)
            
            messages.success(req,"Successfully added staff")
            return HttpResponseRedirect('add_staff')
        except:
            return HttpResponseRedirect('add_staff')
        
def manage_staff(request):
    staffs = models.Instructor.objects.all()  
    return render(request,'App/Admin/manage_staff.html',{'staffs':staffs})

def edit_staff(request,staff_id):
    staffs = models.Instructor.objects.get(user_id=staff_id)
    return render(request,'App/Admin/edit_staff_template.html',{'staffs':staffs})     
def edit_staff_save(request):
    if request.method!='POST':
        return HttpResponse("editing staff is failed")
    else:
        staff_id = request.POST.get('staff_id')
        email = request.POST.get('email')
        fullname = request.POST.get('full_name')
        specialization = request.POST.get('specialization')
        phone = request.POST.get('phone_number')
        
        try:  
            user = models.CustomUser.objects.get(id=staff_id)
            user.email = email
            user.save()
            staff = models.Instructor.objects.get(user_id=staff_id)
            staff.name = fullname
            staff.specialization = specialization
            staff.phone = phone
            staff.save()
            messages.success(request,"Successfully edited staff")
            return HttpResponseRedirect('/edit_staff/'+staff_id)    
        except:
             messages.error(request,"Editing data failed")
             return HttpResponseRedirect('/edit_staff/'+staff_id)