from django.contrib import admin
from company.models import ( Developer,User,
    Teamlead,LeadProjectUpdate,DevProjectUpdate, ProjectAssignment)

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
        model = DevProjectUpdate

admin.site.register(DevProjectUpdate,DvProjectAppAdmin)

class LeadProjectUpdateAdmin(admin.ModelAdmin):

    class Meta:
        model = LeadProjectUpdate

admin.site.register(LeadProjectUpdate,LeadProjectUpdateAdmin)

class ProjectAssignmentAdmin(admin.ModelAdmin):

    class Meta:
        model = ProjectAssignment

admin.site.register(ProjectAssignment,ProjectAssignmentAdmin)

class UserAdmin(admin.ModelAdmin):

    class Meta:
        model = User

admin.site.register(User,UserAdmin)


