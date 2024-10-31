from datetime import timedelta
import json
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required 
from django.views.decorators.cache import never_cache

from App.models import ClassSchedule


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
    
