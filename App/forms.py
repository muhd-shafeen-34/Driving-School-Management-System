from django import forms
from datetime import date

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