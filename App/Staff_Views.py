from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from App import models


@never_cache
@login_required(login_url='login')
def staff_dashboard(req):
    if req.user.role == 'instructor':
        return render(req, 'App/Staff/staff_dashboard.html')
    else:
        return HttpResponseForbidden("you do not have permission to this page")
def instructor_profile(request):
    return render(request,'App/Staff/instructor_profile_template.html')


def students_under_instructor(request):

    students = models.Student.objects.filter(instructor = request.user.instructor)
    return render(request,'App/Staff/students_under_instructor_template.html',{'students':students})
    