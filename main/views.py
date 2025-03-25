from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.views.generic import TemplateView
from .forms import UserRegistrationForm
from .models import UserProfile, Transportation

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
