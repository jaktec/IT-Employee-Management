from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView
from django.views import View
from ..decorators import developer_required
from ..forms import StdProjectAppForm,DeveloperSignUpForm,AdminSignUpForm, ProjectAssignForm
from ..models import Teamlead,Developer, User , TeamProjectApp,Admin, DeveloperProjectApp, ProjectAssignment


class AdminSignUpView(CreateView):
    model = User
    form_class = AdminSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'admin'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('adminpage')

def Adpage(request):

    context = {'ad':'Hello'}

    return render(request,'Adpage.html',context)



def ShowTeamleadApp(request): # show proj snd from teamleads
    
    admin = Admin.objects.filter(user=request.user).first()
    app = TeamProjectApp.objects.filter(to_admin = admin).all()
    
    app2 = TeamProjectApp.objects.filter(id=request.POST.get('answer')).all()

    for items in app2:

        items.status = request.POST.get('status')
        items.save()

    context = { 'app':app }

    return render(request,'showTeamleadApp.html',context)

def AddProjectAssignment(request): # add proj 
    
    form = ProjectAssignForm(request.POST)
    admin = Admin.objects.filter(user=request.user).first()

    if form.is_valid():
        form.instance.user = admin
        form.save()

    context2 = {'form':form}

    return render(request,'assignProject.html',context2)
