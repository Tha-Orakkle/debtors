from django import forms

from .models import User


class UserCreationForm(forms.ModelForm):
        
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "other_name",
                  "email", "telephone", "password")
