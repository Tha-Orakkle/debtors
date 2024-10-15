from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, Organisation


class CustomUserCreationForm(UserCreationForm):
        
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "other_name",
                  "email", "telephone", "password1", "password2"]


class CreateOrganisationForm(forms.ModelForm):
    class Meta:
        model = Organisation
        fields = ["name", "email", "address"]
        

class UpdateOrganisationForm(forms.ModelForm):
    class Meta:
        model = Organisation
        fields = ["name", "email", "address", "telephone"]