
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseForbidden, HttpResponseRedirect
from App import forms, models
from App.models import CustomUser
from django.urls import reverse 
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
        if hasattr(user, 'student'):
            # Check if the student is approved
            if user.student.is_approved:
                return redirect('student_home')  # Redirect to the student dashboard
            else:
                # Redirect to a page informing them that approval is pending
                return redirect('waiting_page')  # Redirect to the pending student dashboard
    else:
        return redirect('/')  # Default redirect if no specific role is found

def waiting_page(request):
    return render(request,'App/500.html')

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


def student_register(request):
    package_details = models.Package.objects.all()
    package_choices = [(package.id, package.name) for package in package_details]  # Prepare choices in (id, name) format
    form = forms.StudentRegistrationForm(package_choices = package_choices)
    
    return render(request, 'App/register.html', {'form': form,'package':package_details})
   
def save_student(request):
    package_details = models.Package.objects.all()
    package_choices = [(package.id, package.name) for package in package_details]
    if request.method == 'POST':
        form = forms.StudentRegistrationForm(request.POST,request.FILES)
        form.fields['package'].choices = package_choices
        if form.is_valid():
            fullname = form.cleaned_data.get('fullname')
            email = form.cleaned_data.get('Email')
            password = form.cleaned_data.get('Password')
            address = form.cleaned_data.get('address')
            phone = form.cleaned_data.get('phone_number')
            
            date_of_birth = form.cleaned_data.get('date_of_birth') 
            package = form.cleaned_data.get('package')
            profile_pic = form.cleaned_data.get('profile_pic')
            proof = form.cleaned_data.get('proof')
            
            # Form is valid, process the data and save it
            user = models.CustomUser.objects.create_user(email=email,password=password,role="student")
            student = models.Student.objects.create(user=user, name=fullname, address=address, phone=phone, dob=date_of_birth,package=models.Package.objects.get(id=package),profile_picture=profile_pic,proof=proof)
            # Example: Create user and student profile here
            return HttpResponseRedirect('login')
        else:
            return HttpResponse(form.errors)
    return render(request, 'App/register.html', {'form': form})