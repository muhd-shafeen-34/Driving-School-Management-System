from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
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

def delete_staff(request,staff_id):
    staff = models.Instructor.objects.get(user_id=staff_id)
    staff.user.delete()
    return HttpResponseRedirect(reverse(manage_staff))



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
    
def add_package(request):
    return render(request, 'App/Admin/add_package_template.html')

def add_package_save(req):
    if req.method != 'POST':
        return HttpResponse("adding package is failed")
    else:
        name = req.POST.get('name')
        desc = req.POST.get('desc')
        price = req.POST.get('price')
        duration = req.POST.get('duration')
        try:
            package = models.Package.objects.create(name=name, description=desc, price=price, duration=duration)
            package.save()
            
            messages.success(req,"Successfully added package")
            return HttpResponseRedirect('add_package')
        except:
            return HttpResponseRedirect('add_package')


def manage_package(request):
    packages = models.Package.objects.all()  
    return render(request,'App/Admin/manage_package_template.html',{'packages':packages})

def edit_package(request,package_id):
    packages = models.Package.objects.get(id=package_id)
    return render(request,'App/Admin/edit_package_template.html',{'packages':packages})


def edit_package_save(request):
    if request.method != 'POST':
        return HttpResponse("Editing package Failed")
    else:
        try:
            pack_id = request.POST.get('pack_id')
            name = request.POST.get('name')
            desc = request.POST.get('desc')
            price = request.POST.get('price')
            duration = request.POST.get('duration')
            package = models.Package.objects.get(id=pack_id)
            package.name = name
            package.description = desc
            package.price = price
            package.duration = duration
            package.save()
            messages.success(request,"Successfully edited package")
            return HttpResponseRedirect('/edit_staff/'+pack_id)
        except:
            messages.error(request,"Editing data failed")
            return HttpResponseRedirect('/edit_staff/'+pack_id)
        
        
        
        
    
def assign_staff_package(request,package_id):
    pack_id = get_object_or_404(models.Package, id=package_id)
    staffs = models.Instructor.objects.all()
    context = {'staffs':staffs,
               'pack_id':pack_id,
            }
               
    return render(request,'App/Admin/assign_staff_package.html',context)







def assign_this_instructor(request,package_id,staff_id):
        package = models.Package.objects.get(id=package_id)
        instructor = models.Instructor.objects.get(user_id=staff_id)  # Assuming 'staff_id' is the 'user.id'
        package.instructor = instructor
        package.save()
        messages.success(request,"Successfully assigned instructor")
        return HttpResponseRedirect(reverse('manage_package'))
    
def students_under_this_package(request,package_id):
    package = models.Package.objects.get(id=package_id)
    student = models.Student.objects.filter(package=package_id)
    return render(request,'App/Admin/students_under_template.html',{'package':package,'student':student})

def pending_student(request):
    students = models.Student.objects.filter(is_approved=False)
    return render(request,'App/Admin/pending_student_template.html',{"students":students})

def approve_student(request,student_id):
    student = models.Student.objects.get(user_id=student_id)
    student.is_approved = True
    student.save()
    return HttpResponseRedirect(reverse('pending_student'))

def reject_student(request,student_id):
    student = models.Student.objects.get(user_id=student_id)
    student.user.delete()
    return HttpResponseRedirect(reverse(pending_student))
    




def manage_student(request):
    students = models.Student.objects.filter(is_approved=True)
    return render(request,'App/Admin/manage_student_template.html',{"students":students})

def delete_student(request,student_id):
    student = models.Student.objects.get(user_id=student_id)
    student.user.delete()
    return HttpResponseRedirect(reverse(manage_student))
    
    
def edit_student(request,student_id):
    students = models.Student.objects.get(user_id=student_id)
    return render(request,'App/Admin/edit_student_template.html',{"students":students})

def edit_student_save(request):
    if request.method!='POST':
        return HttpResponse("editing student is failed")
    else:
        try:
            student_id = request.POST.get('student_id')
            email = request.POST.get('email')
            fullname = request.POST.get('fullname')
            address = request.POST.get('address')
            phone = request.POST.get('phone')
            dob = request.POST.get('dob') 
            user = models.CustomUser.objects.get(id=student_id)
            user.email = email
            user.save()
            student = models.Student.objects.get(user_id=student_id)
            student.name = fullname
            student.address = address
            student.phone = phone
            student.dob = dob
            student.save()
            messages.success(request,"Successfully edited student")
            return HttpResponseRedirect('/edit_student/'+student_id)    
        except:
             messages.error(request,"Editing data failed")
             return HttpResponseRedirect('/edit_student/'+student_id)
    
    
def assign_staff_student(request,student_id):
    student_id = get_object_or_404(models.Student, user_id=student_id)
    staffs = models.Instructor.objects.all()
    context = {'staffs':staffs,
               'student_id':student_id,
            }
               
    return render(request,'App/Admin/assign_staff_student.html',context)

def assign_this_instructor_to_student(request,student_id,staff_id):
        student = models.Student.objects.get(user_id=student_id)
        instructor = models.Instructor.objects.get(user_id=staff_id)  # Assuming 'staff_id' is the 'user.id'
        student.instructor = instructor
        student.save()
        messages.success(request,"Successfully assigned instructor")
        return HttpResponseRedirect(reverse('manage_student'))
    