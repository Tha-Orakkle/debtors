from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
        
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "other_name",
                  "email", "telephone", "password1", "password2"]
