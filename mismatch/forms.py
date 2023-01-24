from django import forms
from .models import User
from django.db.models import fields
from django.forms import ModelForm
from phonenumber_field.widgets import PhoneNumberPrefixWidget

# Creating form for registration
class Registration(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    confirmation = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password repeat'}))

class Log_in(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class Change_pass(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Existed password'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}))
    new_pass_conf = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New password repeat'}))
    

class UserForm(forms.ModelForm):
    
    # Form for the User model
    class Meta:

        model = User
        fields = ('first_name', 'last_name', 'gender', 'birthdate', 'city', 'state', 'phone', 'picture')

        GENDER_CHOICES =(
            ("M", "Male"),
            ("F", "Female")
        )

        # Widgets are django build in tools for form fields style and features
        widgets = {
            'gender': forms.RadioSelect(choices= GENDER_CHOICES),
            
            'birthdate': forms.DateInput(attrs={
                'placeholder': "m/d/Y",
            }),
            'phone': PhoneNumberPrefixWidget(),
        }