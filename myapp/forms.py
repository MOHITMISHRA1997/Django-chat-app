from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Userprofile


class Create_users(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','password1','password2']




class Update_profile(forms.ModelForm):
    class Meta:
        model = Userprofile
        fields = ['profile_img']

class Update_user(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']
