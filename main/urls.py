from django.urls import path
from .views import RegistrationView, LoginView, HomeView, LogoutView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", HomeView.as_view(), name="home"), 

] 