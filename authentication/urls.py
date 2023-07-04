from .views import Registration, UsernameValidation, EmailValidation, LoginView, LogoutView
from django.views.decorators.csrf import csrf_exempt
from django.urls import path

urlpatterns = [
    path('register', Registration.as_view(), name="register"),
    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('validate-username', csrf_exempt(UsernameValidation.as_view()), name="validate-username"),
    path('validate-email', csrf_exempt(EmailValidation.as_view()), name='validate-email'),
]