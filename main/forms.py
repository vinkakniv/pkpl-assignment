from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Transportation, Route, Ticket, Payment
from .validators import phone_validator, validate_birth_date, validate_future_date
from datetime import datetime
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator

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

class TicketBookingForm(forms.Form):
    route = forms.ModelChoiceField(
        queryset=Route.objects.filter(is_active=True),
        label="Route",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    departure_date = forms.DateField(
        label="Departure Date",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        validators=[validate_future_date]
    )
    departure_time = forms.ChoiceField(
        label="Departure Time",
        choices=[
            ('08:00', '08:00'),
            ('10:00', '10:00'),
            ('12:00', '12:00'),
            ('14:00', '14:00'),
            ('16:00', '16:00'),
            ('18:00', '18:00'),
            ('20:00', '20:00'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    seat_number = forms.IntegerField(
        label="Seat Number",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '40'}),
        validators=[MinValueValidator(1), MaxValueValidator(40)]
    )

    def clean(self):
        cleaned_data = super().clean()
        route = cleaned_data.get('route')
        departure_date = cleaned_data.get('departure_date')
        departure_time = cleaned_data.get('departure_time')
        seat_number = cleaned_data.get('seat_number')

        if all([route, departure_date, departure_time, seat_number]):
            # Format waktu ke format yang konsisten (HH:MM)
            if ':' not in departure_time:
                departure_time = f"{departure_time}:00"
            
            # Check if the seat is already booked
            existing_ticket = Ticket.objects.filter(
                route=route,
                departure_date=departure_date,
                departure_time=departure_time,
                seat_number=seat_number,
                status__in=['pending', 'paid']  # Check both pending and paid tickets
            ).exists()
            
            if existing_ticket:
                raise forms.ValidationError(
                    "This seat is already booked for the selected date and time. Please choose another seat."
                )

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add data attributes for JavaScript
        if 'route' in self.fields:
            self.fields['route'].widget.attrs.update({
                'data-url': '/get-available-seats/'
            })

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_method']
        widgets = {
            'payment_method': forms.Select(attrs={'class': 'form-select'})
        }
