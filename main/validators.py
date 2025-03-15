from django.core.validators import RegexValidator
from django import forms
from django.utils.timezone import now
import datetime


def validate_birth_date(value):
    min_date = now().date() - datetime.timedelta(days=12*365)
    if value > min_date:
        raise forms.ValidationError("The minimum age is 12 years old.")
    
phone_validator = RegexValidator(
    regex=r'^\+?[1-9]\d{7,14}$',
    message="The phone number must start with a country code and be 8-15 digits long."
)

chassis_number_validator = RegexValidator(
    regex=r'^[A-Z]{5}[A-Z0-9]{10}$',
    message="The chassis number must consist of 5 letters at the beginning, followed by 10 alphanumeric characters."
)

sim_validator = RegexValidator(
    regex=r'^\d{16}$',
    message="The SIM number must consist of 16 digits."
)

