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