from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin.widgets import AdminDateWidget, AdminSplitDateTime, AdminFileWidget
from django.db import transaction
from django.forms.utils import ValidationError

from company.models import (Developer,Teamlead,LeadProjectUpdate
                                ,DevProjectUpdate ,User, Admin,AppStatus, ProjectAssignment)
import random
import string
class TeamleadSignUpForm(UserCreationForm):
    username = forms.CharField(label="Username", strip=True, help_text='Required. 150 characters or fewer.',)
    password2 = forms.CharField(label="Confirm Password", strip=True, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}), help_text='Username and password will be send to your email', )
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=True)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name','last_name',  'email', 'password1' ,'password2' )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.generate_random_password()
        self.fields['password1'].widget.attrs.update({'value': password})
        self.fields['password2'].widget.attrs.update({'value': password})
        
    def generate_random_password(self):
        return ''.join(random.choices(string.digits, k=6))
    
    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teamlead = True
        user.save()
        teamlead = Teamlead.objects.create(user=user)
        return user


class DeveloperSignUpForm(UserCreationForm):
    username = forms.CharField(label="Username", strip=True, help_text='Required. 150 characters or fewer.',)
    password2 = forms.CharField(label="Confirm Password", strip=True, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}), help_text='Username and password will be send to your email', )
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name','last_name',  'email', 'password1' ,'password2' )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.generate_random_password()
        self.fields['password1'].widget.attrs.update({'value': password})
        self.fields['password2'].widget.attrs.update({'value': password})
        
    def generate_random_password(self):
        return ''.join(random.choices(string.digits, k=6))

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
        model = DevProjectUpdate

        fields = ('content', 'to_teamlead')

        widgets = {

            'content': forms.TextInput,

        }

class LeadProjectUpdateForm(forms.ModelForm):
    class Meta:
        model = LeadProjectUpdate
        fields = ('content', 'to_admin',)

        widgets = {
            'content': forms.TextInput
        }

class NewProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewProjectForm, self).__init__(*args, **kwargs)
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

   
class AssignProjectForm(forms.ModelForm):
    # project_name = forms.ChoiceField(choices=[])
    
    class Meta:
        model = ProjectAssignment
        fields = ('developers',)
       
    def __init__(self, *args, **kwargs):
        super(AssignProjectForm, self).__init__(*args, **kwargs)
        self.fields['developers'].widget.attrs.update({'class': 'col-md-7'})

    #     project_names = ProjectAssignment.objects.values_list('project_name', flat=True).distinct()
    #     self.fields['project_name'].choices = [(name, name) for name in project_names]
    #     instance = kwargs.get('instance')
    #     if instance:
    #         developers_already_assigned = instance.developers.all()
    #         self.fields['developers'].queryset = Developer.objects.exclude(id__in=developers_already_assigned)
