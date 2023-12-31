from django.urls import include, path
from django.contrib import admin
from company.views import company, developers, teamleads,Myadmin
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('company.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', company.SignUpView.as_view(), name='signup'),
    path('accounts/signup/developer/', developers.DeveloperSignUpView.as_view(), name='developer_signup'),
    path('accounts/signup/teamlead/', teamleads.TeamleadSignUpView.as_view(), name='teamlead_signup'),
    path('accounts/signup/admin/', Myadmin.AdminSignUpView.as_view(), name='admin_signup'),
    path('developers',developers.Stpage ,name='developers'),
    path('teamleads',teamleads.Tpage ,name='teamleads'),
    path('logout',company.Logout ,name='logout'),
    path('sprojectApp',developers.StProjectApp,name='sprojectApp'),
    path('LeadSubmit',teamleads.LeadSubmit,name='LeadSubmit'),
    path('tprojectApp',teamleads.TProjectApp,name='tprojectApp'),
    path('ShowTResp',developers.StatusOfApp,name='ShowTResp'),
    path('adminpage',Myadmin.Adpage ,name='adminpage'),
    path('ShowTapp',Myadmin.ShowTeamleadApp ,name='ShowTapp'),
    path('AddProj',Myadmin.AddProjectAssignment ,name='AddProj'),
    path('TAppStatus',teamleads.TeamleadStatusOfApp,name='TAppStatus'),

    path('ViewProj', Myadmin.ViewProjectAssignments ,name='ViewProj'),
    path('UserMng', Myadmin.ManageUsers ,name='UserMng'),

    path('AssignProj', teamleads.AssignProject ,name='AssignProj'),

    path('UserProfile',company.Userprofile ,name='UserProfile'),


    
]
