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
from ..forms import StdProjectAppForm,DeveloperSignUpForm
from ..models import Teamlead,Developer, User , LeadProjectUpdate, DevProjectUpdate, ProjectAssignment
from company.views import company

class DeveloperSignUpView(CreateView):
    model = User
    form_class = DeveloperSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Developer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()        
        login(self.request, user)
        password = form.cleaned_data['password1']
        company.send_registration_email(user,password)
        return redirect('developers')

def StProjectApp(request):

    form = StdProjectAppForm(request.POST)
    
    developer = Developer.objects.filter(user=request.user).first()

    if form.is_valid():
        form.instance.user=developer
        form.save()

    context = {'form':form}

    return render(request,'stApp.html',context)

def StatusOfApp(request):

    developer = Developer.objects.filter(user=request.user).first()

    app = DevProjectUpdate.objects.filter(user=developer).all()

    context = { 'app':app }

    return render(request,'devAppStatus.html',context)


def Stpage(request):

    developer = Developer.objects.filter(user=request.user).first()

    app = DevProjectUpdate.objects.filter(user=developer).all()

    dev = Developer.objects.filter(user=request.user).first()
    data = ProjectAssignment.objects.filter(developers = dev).all()

    context = { 'app':app,
               'data':data }

    return render(request,'stpage.html',context)

def ViewDeveloperAssignments(request): # show proj snd from teamleads
    
    dev = Developer.objects.filter(user=request.user).first()
    data = ProjectAssignment.objects.filter(developers = dev).all()
    
    # app2 = LeadProjectUpdate.objects.filter(id=request.POST.get('answer')).all()

    # for items in app2:

    #     items.status = request.POST.get('status')
    #     items.save()

    context = { 'data':data }

    return render(request,'viewleadAssigns.html',context)