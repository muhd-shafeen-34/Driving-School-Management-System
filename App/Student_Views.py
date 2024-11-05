from datetime import date, datetime, timedelta
from http.client import HTTPResponse
import json
import os
from pyexpat.errors import messages
from django.http import HttpResponseForbidden, JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required 
from django.views.decorators.cache import never_cache

from App import models
from App.forms import FeedbackStudentForm
from App.models import ClassSchedule, FeedbackStudent, Student


@never_cache
@login_required(login_url='login')
def student_dashboard(request):
    if request.user.role == 'student':
        student = request.user.student  # Assuming a related Student model
    schedules = ClassSchedule.objects.filter(student=student)

    events = []
    for schedule in schedules:
        # Iterate over each day in the date range
        current_date = schedule.start_date
        while current_date <= schedule.end_date:
            day_name = current_date.strftime('%A').lower()  # Get the day name in lowercase
            time_range = getattr(schedule, f'{day_name}_time_range', None)  # Get the time range for the day

            if time_range:
                # Extract the lower and upper bounds of the DateTimeTZRange
                time_start = time_range.lower  # Start time
                time_end = time_range.upper    # End time
                
                # Convert times to strings
                if time_start and time_end:
                    time_start_str = f"{time_start.strftime('%I:%M %p')}"
                    time_end_str = f"{time_end.strftime('%I:%M %p')}"
                else:
                    time_start_str = "No Start Time"
                    time_end_str = "No End Time"

                events.append({
                    'title': f"{schedule.instructor.name}",  # Display the instructor's name
                    'start': current_date.isoformat(),       # Use the date as the start time
                    'extendedProps': {
                        'time_range': time_start_str + "<br>" + time_end_str,  # Concatenate with line break
                    }
                })
            current_date += timedelta(days=1)  # Move to the next day

        return render(request, 'App/Student/student_dashboard.html',{'events': json.dumps(events)})
    else:
        return HttpResponseForbidden("you do not have permission to this page")
    

def student_profile(request):
    student_details = get_object_or_404(models.Student,user = request.user)
    
    
    dob = student_details.dob
    if dob:
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    else:
        age = None
    context = { 'student' : student_details,
               'age':age
    }

    return render(request,'App/Student/student_profile_template.html',context)


def student_edit_profile(request,student_id):
    student = get_object_or_404(models.Student,user = student_id)
    return render(request,'App/Student/edit_student_profile_template.html',{'student':student})


def save_student_profile(request):
    if request.method!='POST':
        return HTTPResponse("editing profile is failed")
    else:
        std_id = request.POST.get('student_id')
        email = request.POST.get('email')
        fullname = request.POST.get('full_name')
        address = request.POST.get('address')
        phone = request.POST.get('phone_number')
        dob = request.POST.get('dob')
        profile_pic = request.FILES.get('profile_picture')
        
        try:  
            user = models.CustomUser.objects.get(id=std_id)
            user.email = email
            user.save()
            student = models.Student.objects.get(user_id=std_id)
            student.name = fullname
            student.address = address
            student.phone = phone
            student.dob = dob
            if profile_pic:
                os.path.isfile(student.profile_picture.path)
                os.remove(student.profile_picture.path)
                student.profile_picture = profile_pic
            else:
                pass  # Update the picture
            student.save()
            #messages.success(request,"Successfully edited profile")
            return HttpResponseRedirect('/student_profile')    
        except:
             #messages.error(request,"Editing data failed")
             return HttpResponseRedirect('/edit_profile_instructor/'+std_id)
    
    
    
def student_instructor(request):
    insid = request.user.student.instructor.user_id
    instructor = get_object_or_404(models.Instructor,user_id = insid)
    students_count = models.Student.objects.filter(instructor = instructor).count()
    packages_count = models.Package.objects.filter(instructor = instructor).count()
    context = {
        'instructor':instructor,
        'students_count': students_count,
        'packages_count': packages_count,
        
    }
    return render(request,'App/Student/student_instructor_template.html',context)



def student_feedback(request):
    form = FeedbackStudentForm(request.POST or None)
    student = get_object_or_404(Student,user_id = request.user.id)
    context = {
        'form': form,
        'feedbacks': FeedbackStudent.objects.filter(student=student),
        'page_title': 'Student Feedback'

    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.student = student
                obj.save()
                messages.success(
                    request, "Feedback submitted for review")
                return HttpResponseRedirect('student_feedback')
            except Exception:
                pass#messages.error(request, "Could not Submit!")
        else:
            pass#messages.error(request, "Form has errors!")
    return render(request, "App/Student/student_feedback.html", context)
