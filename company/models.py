from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe


class User(AbstractUser):
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
   

class DeveloperProjectApp(models.Model):

    user = models.ForeignKey(Developer,on_delete='CASCADE')
    to_teamlead = models.ForeignKey(Teamlead,on_delete='CASCADE')
    content = models.CharField(max_length=1000)
    status = models.CharField(max_length=100,null=True)


class AppStatus(models.Model):

    projectApp = models.ForeignKey(DeveloperProjectApp,on_delete='CASCADE')
    status = models.CharField(max_length=100,null=True)


class TeamProjectApp(models.Model):

    user = models.ForeignKey(Teamlead,on_delete='CASCADE')
    to_admin = models.ForeignKey(Admin,on_delete='CASCADE')
    content = models.CharField(max_length=1000)
    status = models.CharField(max_length=100,null=True)
