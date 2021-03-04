from django import forms 
from .models import Lead
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField

User = get_user_model()

class LeadModelForm(forms.ModelForm):

    class Meta:
        model = Lead
        fields = (
            'first_name',
            'last_name',
            'age',
            'agent',   
        ) 

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields=("username",)
        fields_classes = {'username' : UsernameField}