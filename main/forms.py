from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Transportation
from .validators import phone_validator, validate_birth_date
from datetime import datetime

class UserRegistrationForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=16,
        required=True,
        validators=[phone_validator]
    )
    birth_date = forms.DateField(
        required=True,
        validators=[validate_birth_date],
        widget=forms.SelectDateWidget(
            years=range(2025, 1899, -1),
            attrs={'class': 'form-select d-inline-block w-auto mx-1'}
        )
    )
    blog_url = forms.URLField(required=True)
    description = forms.CharField(
        widget=forms.Textarea,
        validators=UserProfile._meta.get_field('description').validators,
        required=True
    )
    chassis_number = forms.CharField(
        max_length=15,
        required=True,
        validators=Transportation._meta.get_field('chassis_number').validators
    )
    sim_number = forms.CharField(
        max_length=16,
        required=True,
        validators=Transportation._meta.get_field('sim_number').validators
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
