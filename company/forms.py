from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError

from company.models import (Developer,Teamlead,TeamProjectApp
                                ,DeveloperProjectApp ,User, Admin,AppStatus)


class TeamleadSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teamlead = True
        user.save()
        teamlead = Teamlead.objects.create(user=user)
        return user


class DeveloperSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_developer = True
        user.save()
        developer = Developer.objects.create(user=user)
        return user

class AdminSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        developer = Admin.objects.create(user=user)
        return user

class AppStatusForm(forms.ModelForm):
    class Meta:
        model = AppStatus

        fields = ('status',)

        widgets = {

            'status':forms.TextInput,

        }

class StdProjectAppForm(forms.ModelForm):
    class Meta:
        model = DeveloperProjectApp

        fields = ('content', 'to_teamlead')

        widgets = {

            'content': forms.TextInput,

        }

class TeamProjectAppForm(forms.ModelForm):
    class Meta:
        model = TeamProjectApp
        fields = ('content', 'to_admin',)

        widgets = {
            'content': forms.TextInput
        }
