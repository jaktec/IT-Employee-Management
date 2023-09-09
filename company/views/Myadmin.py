from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView
from django.views import View
from ..decorators import developer_required
from ..forms import StdProjectAppForm,DeveloperSignUpForm,AdminSignUpForm, NewProjectForm
from ..models import Teamlead,Developer, User , LeadProjectUpdate,Admin, DevProjectUpdate, ProjectAssignment
from company.views import company


class AdminSignUpView(CreateView):
    model = User
    form_class = AdminSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Administrator'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()       
        login(self.request, user)
        password = form.cleaned_data['password1']
        company.send_registration_email(user,password)
        return redirect('adminpage')

def Adpage(request):
    new_projects = ProjectAssignment.objects.filter(status=None).count()
    # from django.db.models import Q....new_projects_count = ProjectAssignment.objects.filter(Q(status=None) | Q(status='')).count()
    inprogress = ProjectAssignment.objects.filter(status="inprogress").count()
    user_count = User.objects.count()
    context = {'ad':'Hello',
               'np': new_projects,
               'ip': inprogress,
                'uc': user_count
               }

    return render(request,'Adminpage.html',context)



def ShowTeamleadApp(request): # show proj snd from teamleads
    
    admin = Admin.objects.filter(user=request.user).first()
    app = LeadProjectUpdate.objects.filter(to_admin = admin).all()
    
    app2 = LeadProjectUpdate.objects.filter(id=request.POST.get('answer')).all()

    for items in app2:

        items.status = request.POST.get('status')
        items.save()

    context = { 'app':app }

    return render(request,'showTeamleadApp.html',context)


def AddProjectAssignment(request): # add proj 
    
    form = NewProjectForm(request.POST)
    admin = Admin.objects.filter(user=request.user).first()

    if form.is_valid():
        form.instance.by_admin = admin
        form.save()
        return redirect('adminpage')

    context2 = {'form':form}

    return render(request,'AddProject.html',context2)

def ViewProjectAssignments(request): # show proj snd from teamleads
    
    admin = Admin.objects.filter(user=request.user).first()
    data = ProjectAssignment.objects.filter(by_admin = admin).all()
    
    # app2 = LeadProjectUpdate.objects.filter(id=request.POST.get('answer')).all()

    # for items in app2:

    #     items.status = request.POST.get('status')
    #     items.save()

    context = { 'data':data }

    return render(request,'viewProjects.html',context)

# def ManageUsers()

def ManageUsers(request):
    if request.method == "POST":
        action = request.POST.get("action")
        username = request.POST.get("username")
        try:
            userobj = User.objects.get(username=username)
            developer = Developer.objects.filter(user=userobj).first()
            teamlead = Teamlead.objects.filter(user=userobj).first()

            if action == "change":
                if developer: 
                    userobj.is_developer = False
                    userobj.is_teamlead = True
                    userobj.save()                   
                    Teamlead.objects.create(user=userobj) 
                    developer.delete()
                    # messages.success(request, f"User '{username}' has been promoted to Teamlead.")
                elif teamlead: 
                    userobj.is_developer = True
                    userobj.is_teamlead = False
                    userobj.save()                      
                    Developer.objects.create(user=userobj)
                    teamlead.delete()
                    # messages.success(request, f"User '{username}' has been demoted to Developer.")
                # else:
                #     messages.error(request, f"User '{username}' is not a Developer or Teamlead.")
            elif action == "delete":                
                userobj.delete()
                # messages.success(request, f"User '{username}' has been deleted.")
            # else:
            #     messages.error(request, "Invalid action specified.")

        except User.DoesNotExist:
            messages.error(request, f"User '{username}' does not exist.")

        return redirect("UserMng")
    
    data1 = Teamlead.objects.all()
    data2 = Developer.objects.all()
    context = { 'data1':data1, 'data2':data2 }

    return render(request,'UserManagement.html',context)
    