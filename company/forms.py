from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin.widgets import AdminDateWidget, AdminSplitDateTime, AdminFileWidget
from django.db import transaction
from django.forms.utils import ValidationError

from company.models import (Developer,Teamlead,TeamProjectApp
                                ,DeveloperProjectApp ,User, Admin,AppStatus, ProjectAssignment)


class TeamleadSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=True)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name','last_name',  'email', 'password1' ,'password2' )

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teamlead = True
        user.save()
        teamlead = Teamlead.objects.create(user=user)
        return user


class DeveloperSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name','last_name',  'email', 'password1' ,'password2' )

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

class ProjectAssignForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectAssignForm, self).__init__(*args, **kwargs)
        self.fields['details'].required = False  
        self.fields['start_date'].required = False 
        self.fields['end_date'].required = False 
        self.fields['attachments'].required = False 
    class Meta:
        model = ProjectAssignment
        fields = ('project_name','details', 'to_lead', 'start_date', 'end_date', 'attachments')
        # fields = "__all__"
        widgets = {
            'project_name': forms.TextInput,
            'details': forms.TextInput(),
            'start_date': AdminDateWidget(attrs={'type': 'date'}),
            'end_date': AdminDateWidget(attrs={'type': 'date'}),
            'attachments': AdminFileWidget()
        }

   

