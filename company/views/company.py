from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.contrib.auth.models import User,auth
from django.core.mail import send_mail
from django.conf import settings
import threading
from threading import Thread
from ..models import Notifications
from django import template
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
    
    if request.method == 'POST':
        # Handle password change form submission
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Update the session with the new password hash
            # messages.success(request, 'Your password was successfully updated.')
            return redirect('UserProfile')  # Redirect back to the user profile page
    else:
        password_form = PasswordChangeForm(request.user)

        
    context = { 'user_role': role, 'password_form': password_form}
              
    return render(request, 'userprofile.html', context)
   


def send_registration_email_async(user, password):
    # return
    subject = 'Your Registration Details'
    message = f'Username: {user.username}\nPassword: {password}'
    from_email = settings.EMAIL_HOST_USER 
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

def send_registration_email(user, password):
    # Start a new thread to send the email asynchronously
    thread = threading.Thread(target=send_registration_email_async, args=(user, password))
    thread.start()

register = template.Library()
@register.inclusion_tag('dash.html')
def display_notifications(user):
    notifications = Notifications.objects.filter(user=user)
    return {'notifications': notifications}