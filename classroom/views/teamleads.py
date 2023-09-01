from django.forms.formsets import formset_factory
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from ..decorators import teamlead_required
from ..forms import TeamProjectAppForm,TeamleadSignUpForm,TeamProjectAppForm,AppStatusForm
from ..models import  User,Teamlead,DeveloperProjectApp,Developer,TeamProjectApp


class TeamleadSignUpView(CreateView):
    model = User
    form_class = TeamleadSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teamlead'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('teamleads')

#def TeamProjectApp(request):

#    form = StdProjectAppForm(request.POST)

 #   if form.is_valid():
  #      form.save()

  #  context = {'form':form}

   # return render(request,'stApp.html',context)


def ShowApp(request): #  showw proj snd from developers
    
    teamlead = Teamlead.objects.filter(user=request.user).first()
    app = DeveloperProjectApp.objects.filter(to_teamlead = teamlead).all()
    app1 = DeveloperProjectApp.objects.filter(to_teamlead = teamlead).all()
    
    app2 = DeveloperProjectApp.objects.filter(id=request.POST.get('answer')).all()

    for items in app2:

        items.status = request.POST.get('status')
        items.save()

    context = { 'app':app }

    return render(request,'ShowApp.html',context)


def Tpage(request):

    context = locals()

    return render(request,'tpage.html',context)


def TProjectApp(request):

    form = TeamProjectAppForm(request.POST)
    teamlead = Teamlead.objects.filter(user=request.user).first()

    if form.is_valid():
        form.instance.user = teamlead
        form.save()

    context = {'form':form}

    return render(request,'tApp.html',context)


def TeamleadStatusOfApp(request):

    teamlead = Teamlead.objects.filter(user=request.user).first()

    app = TeamProjectApp.objects.filter(user=teamlead).all()

    context = { 'app':app }

    return render(request,'TeamleadAppStatus.html',context)


