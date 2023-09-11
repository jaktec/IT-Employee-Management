from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe
from django.core.validators import RegexValidator

class User(AbstractUser):
    email = models.EmailField(unique=True)
    
    is_developer = models.BooleanField(default=False)
    is_teamlead = models.BooleanField(default=False)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone = models.CharField(validators=[phone_regex],max_length=17,blank=True)

class Developer(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    

    def __str__(self):
        return self.user.username


class Teamlead(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    developer = models.ForeignKey(Developer,on_delete=models.CASCADE, null=True)
    

    def __str__(self):
        return self.user.username

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    teamlead = models.ForeignKey(Teamlead,on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username
   

# add data models



    
class ProjectAssignment(models.Model):
   
    project_name = models.CharField(max_length=100)
    details = models.CharField(null=True, max_length=1000)
    by_admin = models.ForeignKey(Admin,on_delete=models.CASCADE)
    to_lead = models.ForeignKey(Teamlead,on_delete=models.CASCADE, blank=True)
    # developer = models.ForeignKey(Developer, on_delete='CASCADE', null=True)
    developers = models.ManyToManyField(Developer, related_name='assigned_projects', blank=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    attachments = models.FileField(null=True, max_length=1000)
    status = models.CharField(max_length=100,null=True)


class DevProjectUpdate(models.Model):    
    project = models.ForeignKey(ProjectAssignment,on_delete=models.CASCADE)
    user = models.ForeignKey(Developer,on_delete=models.CASCADE)
    to_teamlead = models.ForeignKey(Teamlead,on_delete=models.CASCADE, blank=True)
    remarks = models.CharField(max_length=1000, null=True)
    attachments = models.FileField(null=True, max_length=1000)
    status = models.CharField(max_length=100,null=True)

class AppStatus(models.Model):

    projectApp = models.ForeignKey(DevProjectUpdate,on_delete=models.CASCADE)
    status = models.CharField(max_length=100,null=True)


class LeadProjectUpdate(models.Model):
    project = models.ForeignKey(ProjectAssignment,on_delete=models.CASCADE)
    user = models.ForeignKey(Teamlead,on_delete=models.CASCADE)
    to_admin = models.ForeignKey(Admin,on_delete=models.CASCADE, blank = True)
    remarks = models.CharField(max_length=1000, null=True)
    status = models.CharField(max_length=100,null=True)
    attachments = models.FileField(null=True, max_length=1000)