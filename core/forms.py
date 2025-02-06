from django import forms
from .models import Tasks
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate

class CreateForm(forms.ModelForm):
    class Meta:
        model=Tasks
        fields='__all__'

class Registerform(forms.Form):
    name = forms.CharField(max_length=100, label="Your Name")
    email = forms.EmailField(label="Your Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Your Password")
    re_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password') 
        re_password = cleaned_data.get('re_password')  

        if password and re_password and password != re_password:
            raise forms.ValidationError("Passwords do not match.")

class LoginForm(forms.Form):
    email = forms.EmailField(label="Your Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Your Password")

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            # Check if the user exists by email (as email is not the default username)
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError("No such email registered.")

            # Authenticate using the user's username and password
            user = authenticate(username=user.username, password=password)

            if user is None:
                raise forms.ValidationError("Invalid email or password.")
            
            cleaned_data['user'] = user
        return cleaned_data
