from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from validate_email import validate_email  
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views import View
from django.urls import reverse
from django.contrib import auth
import json


class EmailValidation(View):
    def post(self, request):
        data=json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error':'Email is invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'sorry email is in use , choose another one'}, status=409)
        return JsonResponse({'email_valid': True})
    

class UsernameValidation(View):
    def post(self, request):
        data=json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error':'username should only contain alphanumeric characters'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'sorry username is in use , choose another one'}, status=409)
        return JsonResponse({'username_valid': True})

class Registration(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    
    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password is to short')
                    return render(request, 'authentication/register.html', context)
                
                users = User.objects.create_user(username=username, email=email)
                users.set_password(password)
                users.is_active = False
                users.save()
                email_subject = "Activate your account"
                email_body = "Test"
                email = EmailMessage(
                    email_subject,
                    email_body,
                    'noreply123@semicolon.com'
                    [email],
                )
                email.send(fail_silently=False)
                messages.success(request, 'Account successfully Created')
                return render(request, 'authentication/register.html')
        return render(request, 'authentication/register.html')
    
class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    
    def post(self, request):
        username=request.POST['username']
        password=request.POST['password']
        if username and password:
            user=auth.authenticate(request, username=username, password=password)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome, ' + user.username + ' you are now logged in')
                return redirect('expenses')
            messages.error(request, 'Invalid credentials, try again')
            return render(request, 'authentication/login.html')
        return render(request, 'authentication/login.html')
    

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('login')