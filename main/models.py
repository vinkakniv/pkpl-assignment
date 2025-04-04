from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator
from .validators import chassis_number_validator, sim_validator, phone_validator

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_regex = models.CharField(max_length=16, validators=[phone_validator])
    birth_date = models.DateField()
    blog_url = models.URLField()
    description = models.TextField(validators=[MinLengthValidator(5), MaxLengthValidator(1000)])

    def __str__(self):
        return self.user.username

class Transportation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    chassis_number = models.CharField(validators=[chassis_number_validator], max_length=15, unique=True)
    sim_number = models.CharField(validators=[sim_validator], max_length=16, unique=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.chassis_number}"

# Master Table
class Route(models.Model):
    code = models.CharField(max_length=10, unique=True)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    distance = models.DecimalField(max_digits=10, decimal_places=2)  
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.origin} - {self.destination}"

# Transaction Table 1: Ticket
class Ticket(models.Model):
    TICKET_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]

    ticket_number = models.CharField(max_length=10, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    departure_date = models.DateField()
    departure_time = models.CharField(max_length=5)
    seat_number = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=TICKET_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ticket_number} - {self.user.username}"

    @classmethod
    def is_seat_available(cls, route, departure_date, departure_time, seat_number):
        # Check if the seat is already booked for the same route, date, and time
        existing_ticket = cls.objects.filter(
            route=route,
            departure_date=departure_date,
            departure_time=departure_time,
            seat_number=seat_number,
            status__in=['pending', 'paid']  # Only check active tickets
        ).exists()
        
        return not existing_ticket

    @classmethod
    def get_available_seats(cls, route, departure_date, departure_time):
        all_seats = set(range(1, 41))
        
        # Get booked seats for the same route, date, and time
        booked_seats = set(cls.objects.filter(
            route=route,
            departure_date=departure_date,
            departure_time=departure_time,
            status__in=['pending', 'paid']
        ).values_list('seat_number', flat=True))
        
        # Return available seats
        return list(all_seats - booked_seats)

# Transaction Table 2: Payment
class Payment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('CASH', 'Cash'),
        ('BANK_TRANSFER', 'Bank Transfer'),
        ('E_WALLET', 'E-Wallet'),
        ('CREDIT_CARD', 'Credit Card'),
    ]

    payment_number = models.CharField(max_length=20, unique=True)
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    payment_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.payment_number} - {self.ticket.ticket_number}"