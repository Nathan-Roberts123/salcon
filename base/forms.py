from django import forms
from .models import User, country, Address
#from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=50)


class registerForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email','password1','password2']

class addressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = "__all__"




""" 
class registerForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']
"""
