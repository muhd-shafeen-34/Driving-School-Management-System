import datetime
import os
from pyexpat.errors import messages
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.cache import never_cache
from psycopg2.extras import DateTimeTZRange
from App import models
from App.forms import ClassScheduleForm, FeedbackStaffForm


@never_cache
@login_required(login_url='login')
def staff_dashboard(req):
    if req.user.role == 'instructor':
        return render(req, 'App/Staff/staff_dashboard.html')
    else:
        return HttpResponseForbidden("you do not have permission to this page")
def instructor_profile(request):
    instructor_details = get_object_or_404(models.Instructor,user = request.user)
    students_count = models.Student.objects.filter(instructor = request.user.instructor).count()
    packages_count = models.Package.objects.filter(instructor = request.user.instructor).count()
    context = {
        'instructor':instructor_details,
        'students_count':students_count,
        'packages_count':packages_count,
    }
    return render(request,'App/Staff/instructor_profile_template.html',context)

def edit_profile_instructor(request,staff_id):
    instructor = get_object_or_404(models.Instructor, user=staff_id)
    return render(request,'App/Staff/edit_profile_instructor.html',{'staffs':instructor})

def save_instructor_profile(request):
    if request.method!='POST':
        return HttpResponse("editing profile is failed")
    else:
        staff_id = request.POST.get('staff_id')
        email = request.POST.get('email')
        fullname = request.POST.get('full_name')
        specialization = request.POST.get('specialization')
        phone = request.POST.get('phone_number')
        profile_pic = request.FILES.get('profile_picture')
        
        try:  
            user = models.CustomUser.objects.get(id=staff_id)
            user.email = email
            user.save()
            staff = models.Instructor.objects.get(user_id=staff_id)
            staff.name = fullname
            staff.specialization = specialization
            staff.phone = phone
            if profile_pic:
                os.path.isfile(staff.profile_picture.path)
                os.remove(staff.profile_picture.path)
                staff.profile_picture = profile_pic
            else:
                pass  # Update the picture
            staff.save()
            #messages.success(request,"Successfully edited profile")
            return HttpResponseRedirect('/edit_profile_instructor/'+staff_id)    
        except:
             #messages.error(request,"Editing data failed")
             return HttpResponseRedirect('/edit_profile_instructor/'+staff_id)



def students_under_instructor(request):

    students = models.Student.objects.filter(instructor = request.user.instructor)
    return render(request,'App/Staff/students_under_instructor_template.html',{'students':students})


def assign_class_schedule_form(request,staff_id,student_id):
    std_id = student_id
    staf_id = staff_id
    form = ClassScheduleForm()
    context = {'form':form,'student_id':std_id,'staff_id':staf_id}
    return render(request, 'App/Staff/assign_class_timings.html', context)




def save_class_schedule(request):
    if request.method != 'POST':
        return HttpResponse("editing staff is failed")
    else:
        form = ClassScheduleForm(request.POST)
        if form.is_valid():
            # Get the form data directly from cleaned_data
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            student = request.POST.get('student_id')
            instructor = request.POST.get('staff_id'),
            monday_time_range = form.cleaned_data.get('monday_time_range')
            tuesday_time_range = form.cleaned_data.get('tuesday_time_range')
            wednesday_time_range = form.cleaned_data.get('wednesday_time_range')
            thursday_time_range = form.cleaned_data.get('thursday_time_range')
            friday_time_range = form.cleaned_data.get('friday_time_range')
            saturday_time_range = form.cleaned_data.get('saturday_time_range')

            # Create the ClassSchedule instance and save it to the database
            models.ClassSchedule.objects.create(
                student= get_object_or_404(models.Student, user_id=student),
                instructor=get_object_or_404(models.Instructor, user_id=instructor),
                start_date=start_date,
                end_date=end_date,
                monday_time_range=monday_time_range,
                tuesday_time_range=tuesday_time_range,
                wednesday_time_range=wednesday_time_range,
                thursday_time_range=thursday_time_range,
                friday_time_range=friday_time_range,
                saturday_time_range=saturday_time_range,
            )
            return HttpResponseRedirect(reverse('students_under_instructor'))  # Replace with your desired redirect URL
        else:
            print("Form Errors:", form.errors)
            return HttpResponse("assigning timings is failed due to form is not valid")
        
        


def staff_feedback(request):
    form = FeedbackStaffForm(request.POST or None)
    instructor = get_object_or_404(models.Instructor,user_id=request.user.id)
    context = {
        'form': form,
        'feedbacks': models.FeedbackStaff.objects.filter(instructor=instructor),
        'page_title': 'Add Feedback'
    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.instructor = instructor
                obj.save()
                messages.success(request, "Feedback submitted for review")
                return HttpResponseRedirect('instructor_sent_feedback')
            except Exception:
                messages.error(request, "Could not Submit!")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "App/Staff/instructor_feedback.html", context)
