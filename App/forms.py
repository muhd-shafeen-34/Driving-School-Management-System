from django import forms

class CustomLoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100,widget=forms.TextInput(attrs={
        'class': 'form-control',  # Add your desired class here
        'placeholder': 'Email'
    }))
    password = forms.CharField(label="Password",widget=forms.PasswordInput(attrs={
        'class': 'form-control',  # Add your desired class here
        'placeholder': 'Enter your password'
    }))
    
