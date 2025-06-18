from django.contrib import admin

from main.models import UserProfile, Transportation, Ticket, Payment, Route

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Transportation)
admin.site.register(Ticket)
admin.site.register(Payment)
admin.site.register(Route)