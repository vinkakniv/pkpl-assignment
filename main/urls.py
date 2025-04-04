from django.urls import path
from .views import (
    RegistrationView, HomeView, LoginView, LogoutView,
    TicketBookingView, PaymentView, get_available_seats, TicketDetailView, TicketListView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('book-ticket/', TicketBookingView.as_view(), name='book_ticket'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('ticket/<int:pk>/', TicketDetailView.as_view(), name='ticket_detail'),
    path('tickets/', TicketListView.as_view(), name='ticket_list'),
    path('get-available-seats/', get_available_seats, name='get_available_seats'),
] 