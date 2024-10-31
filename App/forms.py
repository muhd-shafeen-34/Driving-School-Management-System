from django import forms
from datetime import date, datetime, timedelta
from psycopg2.extras import DateTimeTZRange  # Needed to set time ranges
from App.models import ClassSchedule

class CustomLoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100,widget=forms.TextInput(attrs={
        'class': 'form-control',  # Add your desired class here
        'placeholder': 'Email'
    }))
    password = forms.CharField(label="Password",widget=forms.PasswordInput(attrs={
        'class': 'form-control',  # Add your desired class here
        'placeholder': 'Enter your password'
    }))
    


class StudentRegistrationForm(forms.Form):
    fullname = forms.CharField(max_length=100,widget=forms.TextInput(attrs={
        'class': 'form-control',  # Add your desired class here
        'placeholder': 'Full Name'
    }))
    Email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'form-control',  # Add your desired class here
        'placeholder': 'Email'
    }))
    Password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',  # Add your desired class here
        'placeholder': 'password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',  # Add your desired class here
        'placeholder': 'Confirm Password'
    }))
    address = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',  # Add your desired class here
        'placeholder': 'Address'
    }))
    phone_number = forms.CharField(max_length=15, required=True,widget=forms.TextInput(attrs={
        'class': 'form-control',  # Add your desired class here
        'placeholder': 'phone number'
    }))
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, date.today().year),attrs={
        'class': 'form-control'
    }))
    package = forms.ChoiceField(choices=[], widget=forms.Select(attrs={
        'class': 'form-control'
     }))
    profile_pic = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'form-control',  # Add your desired class here
        'placeholder': 'add profile pic'
    }))
    proof = forms.FileField(widget=forms.FileInput(attrs={
        'class': 'form-control',  # Add your desired class here
        'placeholder': 'add ID - Proof'
    }),required=True)

    
    
    # Validate that the user is at least 18 years old
    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        if dob:
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age < 18:
                raise forms.ValidationError("You must be at least 18 years old to register.")
        return dob

    # Validate that password and confirm_password match
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("Password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                 self.add_error('confirm_password', "Passwords do not match.") 

        return cleaned_data
    
    
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')

        if not phone:
            raise forms.ValidationError("Phone number is required.")

        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")

        if len(phone) < 10:
            raise forms.ValidationError("Phone number must be at least 10 digits.")

        return phone
    
# Override the init method to accept dynamic package choices
    def __init__(self, *args, **kwargs):
        package_choices = kwargs.pop('package_choices', [])
        super(StudentRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['package'].choices = package_choices
        
        
        





class ClassScheduleForm(forms.ModelForm):
    # Start and end date fields
    start_date = forms.DateField(
        initial=date.today,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'placeholder': 'Select Start Date',
            'style': 'width: 100%; border-radius: 5px;'
        })
    )
    end_date = forms.DateField(
        initial=date.today() + timedelta(days=7),
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'placeholder': 'Select End Date',
            'style': 'width: 100%; border-radius: 5px;'
        })
    )

    # Fields for each day's start and end times
    monday_start = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'placeholder': 'Monday Start Time'}))
    monday_end = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'placeholder': 'Monday End Time'}))
    tuesday_start = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'placeholder': 'Tuesday Start Time'}))
    tuesday_end = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'placeholder': 'Tuesday End Time'}))
    wednesday_start = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'placeholder': 'Wednesday Start Time'}))
    wednesday_end = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'placeholder': 'Wednesday End Time'}))
    thursday_start = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'placeholder': 'Thursday Start Time'}))
    thursday_end = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'placeholder': 'Thursday End Time'}))
    friday_start = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'placeholder': 'Friday Start Time'}))
    friday_end = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'placeholder': 'Friday End Time'}))
    saturday_start = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'placeholder': 'Saturday Start Time'}))
    saturday_end = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'placeholder': 'Saturday End Time'}))

    class Meta:
        model = ClassSchedule
        fields = [
            'start_date', 'end_date',
            'monday_time_range', 'tuesday_time_range', 'wednesday_time_range',
            'thursday_time_range', 'friday_time_range', 'saturday_time_range',
        ]

    def clean(self):
        cleaned_data = super().clean()

        # Days and respective fields for start and end times
        days = {
            'monday': ('monday_start', 'monday_end', 'monday_time_range'),
            'tuesday': ('tuesday_start', 'tuesday_end', 'tuesday_time_range'),
            'wednesday': ('wednesday_start', 'wednesday_end', 'wednesday_time_range'),
            'thursday': ('thursday_start', 'thursday_end', 'thursday_time_range'),
            'friday': ('friday_start', 'friday_end', 'friday_time_range'),
            'saturday': ('saturday_start', 'saturday_end', 'saturday_time_range'),
        }

        for day, (start_field, end_field, range_field) in days.items():
            start_time = cleaned_data.get(start_field)
            end_time = cleaned_data.get(end_field)

            if start_time and end_time:
                # Validate that start time is before end time
                if start_time >= end_time:
                    self.add_error(start_field, f"{day.capitalize()} start time must be before end time.")
                    self.add_error(end_field, f"{day.capitalize()} end time must be after start time.")
                else:
                    # Set the range field if start and end times are valid
                    cleaned_data[range_field] = DateTimeTZRange(
                        datetime.combine(datetime.today(), start_time),
                        datetime.combine(datetime.today(), end_time)
                    )

        return cleaned_data