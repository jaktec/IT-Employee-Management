from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_developer = models.BooleanField(default=False)
    is_teamlead = models.BooleanField(default=False)


class Developer(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    

    def __str__(self):
        return self.user.username


class Teamlead(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    developer = models.ForeignKey(Developer,on_delete='CASCADE', null=True)
    

    def __str__(self):
        return self.user.username

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    teamlead = models.ForeignKey(Teamlead,on_delete='CASCADE', null=True)

    def __str__(self):
        return self.user.username
   

# add data models

class DevProjectUpdate(models.Model):

    user = models.ForeignKey(Developer,on_delete='CASCADE')
    to_teamlead = models.ForeignKey(Teamlead,on_delete='CASCADE')
    content = models.CharField(max_length=1000)
    status = models.CharField(max_length=100,null=True)


class AppStatus(models.Model):

    projectApp = models.ForeignKey(DevProjectUpdate,on_delete='CASCADE')
    status = models.CharField(max_length=100,null=True)


class LeadProjectUpdate(models.Model):

    user = models.ForeignKey(Teamlead,on_delete='CASCADE')
    to_admin = models.ForeignKey(Admin,on_delete='CASCADE')
    content = models.CharField(max_length=1000)
    status = models.CharField(max_length=100,null=True)


    
class ProjectAssignment(models.Model):
   
    project_name = models.CharField(max_length=100)
    details = models.CharField(null=True, max_length=1000)
    user = models.ForeignKey(User,on_delete='CASCADE')
    to_lead = models.ForeignKey(Teamlead,on_delete='CASCADE')
    developer = models.ForeignKey(Developer, on_delete='CASCADE', null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    attachments = models.FileField(null=True, max_length=1000)
    status = models.CharField(max_length=100,null=True)

