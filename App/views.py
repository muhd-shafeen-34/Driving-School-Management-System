from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseForbidden
from App.models import CustomUser
from django.urls import reverse
from App import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages


# Create your views here.
def index(req):
    return render(req,'App/index.html')
# def login(req):
#     return render(req,'App/login.html')

    


def role_based_redirect(user):
    """Redirect users to different pages based on their role."""
    if user.role=='admin':  # Admin user
        return redirect('admin_home') # Redirect to the admin dashboard
    elif user.role == 'instructor':  # Custom role for staff
        return redirect('staff_home')  # Redirect to the staff dashboard
    elif user.role == 'student':  # Custom role for student
        return redirect('student_home')  # Redirect to the student dashboard
    else:
        return redirect('/')  # Default redirect if no specific role is found



def custom_login_view(request):
    if request.method == 'POST':
        form = forms.CustomLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
        
            user = authenticate(request, username=email, password=password)
        
            if user is not None:
                login(request, user)  # Log the user in

            # Call the role-based redirect function
                return role_based_redirect(user)
            else:
                messages.error(request, "Invalid login credentials")
                return redirect('login')
    else:
        form = forms.CustomLoginForm()
    return render(request, 'App/login.html', {'form': form})

def custom_logout(request):
    logout(request)  # This will log out the user
    return redirect('login')  # Redirect to index after logout
