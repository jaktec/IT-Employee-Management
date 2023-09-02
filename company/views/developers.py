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
from ..models import Teamlead,Developer, User , TeamProjectApp, DeveloperProjectApp


class DeveloperSignUpView(CreateView):
    model = User
    form_class = DeveloperSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'developer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
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

    app = DeveloperProjectApp.objects.filter(user=developer).all()

    context = { 'app':app }

    return render(request,'AppStatus.html',context)


def Stpage(request):

    developer = Developer.objects.filter(user=request.user).first()

    app = DeveloperProjectApp.objects.filter(user=developer).all()

    context = { 'app':app }

    return render(request,'stpage.html',context)
