from django.contrib import admin
from company.models import ( Developer,User,
    Teamlead,TeamProjectApp,DeveloperProjectApp, ProjectAssignment)

# Register your models here.

class TeamAdmin(admin.ModelAdmin):

    class Meta:
        model = Teamlead

admin.site.register(Teamlead,TeamAdmin)

class DevAdmin(admin.ModelAdmin):

    class Meta:
        model = Developer

admin.site.register(Developer,DevAdmin)

class DvProjectAppAdmin(admin.ModelAdmin):

    class Meta:
        model = DeveloperProjectApp

admin.site.register(DeveloperProjectApp,DvProjectAppAdmin)

class TeamProjectAppAdmin(admin.ModelAdmin):

    class Meta:
        model = TeamProjectApp

admin.site.register(TeamProjectApp,TeamProjectAppAdmin)

class ProjectAssignmentAdmin(admin.ModelAdmin):

    class Meta:
        model = ProjectAssignment

admin.site.register(ProjectAssignment,ProjectAssignmentAdmin)

class UserAdmin(admin.ModelAdmin):

    class Meta:
        model = User

admin.site.register(User,UserAdmin)


