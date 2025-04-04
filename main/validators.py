from django.core.validators import RegexValidator
from django import forms
from django.utils.timezone import now
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_birth_date(value):
    min_date = now().date() - datetime.timedelta(days=12*365)
    if value > min_date:
        raise forms.ValidationError("The minimum age is 12 years old.")
    
def validate_future_date(value):
    if value < datetime.now().date():
        raise ValidationError(
            _('Departure date cannot be in the past'),
            code='invalid_date'
        )

def validate_future_time(value):
    if value < datetime.now().time():
        raise ValidationError(
            _('Departure time cannot be in the past'),
            code='invalid_time'
        )

def validate_seat_availability(value):
    if value < 1 or value > 40:
        raise ValidationError(
            _('Invalid seat number'),
            code='invalid_seat'
        )

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

