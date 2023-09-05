from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.contrib.auth.models import User,auth


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
   