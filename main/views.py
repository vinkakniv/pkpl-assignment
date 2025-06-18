from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.db import transaction
from .forms import UserRegistrationForm, TicketBookingForm, PaymentForm
from .models import UserProfile, Transportation, Route, Ticket, Payment
import uuid
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy

class RegistrationView(FormView):
    template_name = "registration.html"
    form_class = UserRegistrationForm
    success_url = "/login/" 

    def form_valid(self, form):
        user = form.save()
        
        UserProfile.objects.create(
            user=user,
            phone_regex=form.cleaned_data["phone_number"],
            birth_date=form.cleaned_data["birth_date"],
            blog_url=form.cleaned_data["blog_url"],
            description=form.cleaned_data["description"],
        )

        Transportation.objects.create(
            user=user,
            chassis_number=form.cleaned_data["chassis_number"],
            sim_number=form.cleaned_data["sim_number"],
        )

        messages.success(self.request, "Registration successful! You may now log in.")
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, "Oops! There was an error in your submission. Please check and try again.")
        return super().form_invalid(form)

class HomeView(TemplateView):
    template_name = "home.html"

class LoginView(FormView):
    template_name = "login.html"
    form_class = AuthenticationForm
    success_url = "/"

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)
            return redirect(self.success_url)
        else:
            messages.error(self.request, "Incorrect username or password. Please try again.")
            return self.form_invalid(form)

class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.info(request, "You have successfully logged out. See you again soon!")
        return redirect("home")

class TicketBookingView(LoginRequiredMixin, FormView):
    template_name = "ticket_booking.html"
    form_class = TicketBookingForm
    success_url = "/payment/"

    def get(self, request, *args, **kwargs):
        # Only delete pending ticket if coming from payment page
        if 'ticket_id' in request.session and request.META.get('HTTP_REFERER', '').endswith('/payment/'):
            try:
                ticket = Ticket.objects.get(id=request.session['ticket_id'])
                if ticket.status == 'pending':
                    ticket.delete()
                del request.session['ticket_id']
            except Ticket.DoesNotExist:
                pass

        return super().get(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        if 'booking_data' in self.request.session:
            initial.update(self.request.session['booking_data'])
        return initial

    def form_valid(self, form):
        with transaction.atomic():
            # Generate unique ticket number
            ticket_number = f"TKT{str(uuid.uuid4())[:6].upper()}"
            
            # Get route and calculate price
            route = form.cleaned_data['route']
            price = route.base_price  
            
            departure_time = form.cleaned_data['departure_time']
            if ':' not in departure_time:
                departure_time = f"{departure_time}:00"
            
            # Create ticket
            ticket = Ticket.objects.create(
                ticket_number=ticket_number,
                user=self.request.user,
                route=route,
                departure_date=form.cleaned_data['departure_date'],
                departure_time=departure_time,
                seat_number=form.cleaned_data['seat_number'],
                price=price,
                status='pending'
            )
            
            # Store ticket ID in session for payment
            self.request.session['ticket_id'] = ticket.id
            
            # Store booking data in session for potential return
            self.request.session['booking_data'] = {
                'route': form.cleaned_data['route'].id,
                'departure_date': form.cleaned_data['departure_date'].isoformat(),
                'departure_time': departure_time,
                'seat_number': form.cleaned_data['seat_number']
            }
            
        return super().form_valid(form)

class PaymentView(LoginRequiredMixin, FormView):
    template_name = 'payment.html'
    form_class = PaymentForm
    success_url = reverse_lazy('ticket_detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket_id = self.request.session.get('ticket_id')
        if ticket_id:
            try:
                ticket = Ticket.objects.get(id=ticket_id)
                context['ticket'] = ticket
            except Ticket.DoesNotExist:
                messages.error(self.request, "Ticket not found.")
        else:
            messages.error(self.request, "No ticket found in session.")
        return context

    def form_valid(self, form):
        try:
            with transaction.atomic():
                # Get ticket from session
                ticket_id = self.request.session.get('ticket_id')
                if not ticket_id:
                    messages.error(self.request, "No ticket found in session.")
                    return self.form_invalid(form)

                ticket = Ticket.objects.get(id=ticket_id)
                
                # Generate unique payment number
                payment_number = f"PAY-{uuid.uuid4().hex[:8].upper()}"
                
                # Create payment
                payment = Payment.objects.create(
                    payment_number=payment_number,
                    ticket=ticket,
                    amount=ticket.price,
                    payment_method=form.cleaned_data['payment_method'],
                    status='SUCCESS',
                    payment_date=datetime.now()
                )
                
                # Update ticket status to 'paid' only after successful payment
                ticket.status = 'paid'
                ticket.save()
                
                # Clear session
                del self.request.session['ticket_id']
                
                messages.success(self.request, "Payment successful! Your ticket has been confirmed.")
                # Redirect to the specific ticket detail page
                return redirect('ticket_detail', pk=ticket.id)
                
        except Exception as e:
            messages.error(self.request, f"Error processing payment: {str(e)}")
            return self.form_invalid(form)

@require_GET
def get_available_seats(request):
    route_id = request.GET.get('route_id')
    departure_date = request.GET.get('departure_date')
    departure_time = request.GET.get('departure_time')

    print(f"Received request with route_id: {route_id}, date: {departure_date}, time: {departure_time}")

    if not all([route_id, departure_date, departure_time]):
        return JsonResponse({'error': 'Missing parameters'}, status=400)

    try:
        if ':' not in departure_time:
            departure_time = f"{departure_time}:00"
        
        print(f"Formatted time: {departure_time}")
        
        # Get all seats (1-40)
        all_seats = list(range(1, 41))
        
        booked_seats = list(Ticket.objects.filter(
            route_id=route_id,
            departure_date=departure_date,
            departure_time=departure_time,
            status__in=['pending', 'paid']  # Only check pending and paid tickets
        ).values_list('seat_number', flat=True))
                
        # Return available seats (seats that are not booked)
        available_seats = [seat for seat in all_seats if seat not in booked_seats]
        
        return JsonResponse({'available_seats': available_seats})
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)

class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = 'ticket_detail.html'
    context_object_name = 'ticket'

    def get_object(self):
        ticket_id = self.kwargs.get('pk')
        return Ticket.objects.get(id=ticket_id, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket = context['ticket']
        try:
            payment = Payment.objects.get(ticket=ticket)
            context['payment'] = payment
        except Payment.DoesNotExist:
            context['payment'] = None
        return context

class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'ticket_list.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user).order_by('-departure_date', '-departure_time')
