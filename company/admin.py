from django.contrib import admin
from company.models import ( Developer,User,
    Teamlead,TeamProjectApp,DeveloperProjectApp )

# Register your models here.

class TeamAdmin(admin.ModelAdmin):

    class Meta:
        model = Teamlead

admin.site.register(Teamlead,TeamAdmin)

class StudAdmin(admin.ModelAdmin):

    class Meta:
        model = Developer

admin.site.register(Developer,StudAdmin)

class StProjectAppAdmin(admin.ModelAdmin):

    class Meta:
        model = DeveloperProjectApp

admin.site.register(DeveloperProjectApp,StProjectAppAdmin)

class TeamProjectAppAdmin(admin.ModelAdmin):

    class Meta:
        model = TeamProjectApp

admin.site.register(TeamProjectApp,TeamProjectAppAdmin)


class UserAdmin(admin.ModelAdmin):

    class Meta:
        model = User

admin.site.register(User,UserAdmin)
