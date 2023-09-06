from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.contrib.auth.models import User,auth
from django.core.mail import send_mail
from django.conf import settings
import threading
from threading import Thread

class SignUpView(TemplateView):
    template_name = 'registration/signup.html'

def home(request):
    if request.user.is_authenticated:
        if request.user.is_teamlead:
            return redirect('teamleads')
        elif request.user.is_developer:
            return redirect('developers')
        elif request.user.is_superuser:
            return redirect('adminpage')

    return render(request, 'company/home.html')

def Logout(request):

    auth.logout(request)
    return render(request, 'company/home.html')

def Userprofile(request):
    role = "Administrator"
    if request.user.is_authenticated:
        if request.user.is_teamlead:
            role = "Team Lead"
        elif request.user.is_developer:
            role = "Developer"
        
    context = { 'user_role': role}
              
    return render(request, 'userprofile.html', context)
   

def send_registration_email_async(user, password):
    
    subject = 'Your Registration Details'
    message = f'Username: {user.username}\nPassword: {password}'
    from_email = settings.EMAIL_HOST_USER 
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

def send_registration_email(user, password):
    # Start a new thread to send the email asynchronously
    thread = threading.Thread(target=send_registration_email_async, args=(user, password))
    thread.start()