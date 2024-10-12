from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.contrib.auth.decorators import login_required 

@login_required(login_url='login')
def student_dashboard(req):
    if req.user.role == 'student':
        return render(req, 'App/Student/student_dashboard.html')
    else:
        return HttpResponseForbidden("you do not have permission to this page")