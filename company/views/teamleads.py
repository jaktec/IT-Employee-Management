from django.forms.formsets import formset_factory
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from ..decorators import teamlead_required
from ..forms import LeadProjectUpdateForm,TeamleadSignUpForm,LeadProjectUpdateForm,AppStatusForm, AssignProjectForm
from ..models import  User,Teamlead,DevProjectUpdate,Developer,LeadProjectUpdate, ProjectAssignment, Notifications

from company.views import company
from django.http import FileResponse

class TeamleadSignUpView(CreateView):
    model = User
    form_class = TeamleadSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Team Lead'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):        
        user = form.save()
        admin_users = User.objects.filter(is_staff=True)
        notification = Notifications(content= str(user.username) +"joined as Teamlead")
        notification.save()
        notification.user.add(*admin_users)        
        login(self.request, user)
        password = form.cleaned_data['password1']
        # company.send_registration_email(user,password)
        return redirect('teamleads')

#def LeadProjectUpdate(request):

#    form = StdProjectAppForm(request.POST)

 #   if form.is_valid():
  #      form.save()

  #  context = {'form':form}

   # return render(request,'stApp.html',context)


def LeadSubmit(request): #   proj snd from developers
    teamlead = Teamlead.objects.filter(user=request.user).first()
    devpdate = DevProjectUpdate.objects.filter(to_teamlead = teamlead).all()
    form = LeadProjectUpdateForm(request.POST)
    response = ""
    # if request.method == 'POST':
    for devsubmit in devpdate:
        if devsubmit.attachments:
            file_path = devsubmit.attachments.path
           
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{devsubmit.attachments.name}"'
            # project_assignment.status = request.POST.get('status')
            # project_assignment.save()
        form = LeadProjectUpdateForm(request.POST)
        if form.is_valid():
                
            project_id = request.POST.get('pid')
            paction = request.POST.get('paction')
            passignment = get_object_or_404(ProjectAssignment, id=project_id)
            form.instance.to_admin = passignment.by_admin
            form.instance.user=teamlead
            form.instance.project = passignment
            form.instance.attachments = devsubmit.attachments

                
               
            if paction == "accept":
                passignment.status = "review"
                form.instance.status = "accept"
            elif paction == "reject":
                passignment.status = "inprogress"
                form.instance.status = "reject"
            passignment.save()  
            form.save()
            return redirect('LeadSubmit')  
              
    # for items in app2:

    #     items.status = request.POST.get('status')
    #     items.save()

    context = { 'form':form, 'devupdate':devpdate , 'resp': response}

    return render(request,'LeadSubmission.html',context)


def Tpage(request):

    # context = locals()
    teamlead = Teamlead.objects.filter(user=request.user).first()
    data = ProjectAssignment.objects.filter(to_lead = teamlead).all()
    context = { 'data':data }
    return render(request,'tleadpage.html',context)


def TProjectApp(request):

    form = LeadProjectUpdateForm(request.POST)
    teamlead = Teamlead.objects.filter(user=request.user).first()

    if form.is_valid():
        form.instance.user = teamlead
        form.save()

    context = {'form':form}

    return render(request,'tleadApp.html',context)


def TeamleadStatusOfApp(request):

    teamlead = Teamlead.objects.filter(user=request.user).first()

    app = LeadProjectUpdate.objects.filter(user=teamlead).all()

    context = { 'app':app }

    return render(request,'TeamleadAppStatus.html',context)



def AssignProject(request):
    form = AssignProjectForm(request.POST)   
    teamlead = Teamlead.objects.filter(user=request.user).first()
    pdata = ProjectAssignment.objects.filter(to_lead = teamlead).all()

    # app2 = ProjectAssignment.objects.filter(project_name=request.POST.get('answer')).all()
    if request.method == 'POST':
        for project_assignment in pdata:

            # project_assignment.status = request.POST.get('status')
            # project_assignment.save()
            form = AssignProjectForm(request.POST)
            if form.is_valid():
                
                project_id = request.POST.get('answer')
                project_assignment2 = get_object_or_404(ProjectAssignment, id=project_id)
                project_assignment2.status = "inprogress"
                project_assignment2.developers.set(form.cleaned_data['developers'])
                project_assignment2.save()  

                dev_users = [developer.user for developer in project_assignment2.developers.all()]
                notification = Notifications(content= "Project Assigned by" + str(project_assignment2.to_lead))
                notification.save()
                notification.user.add(*dev_users)    
                # form.save_m2m() 
                return redirect('teamleads')  
    
    
   

    return render(request, 'tAssignProject.html', {'form': form, 'data': pdata})

# def AssignProject(request): # show proj snd from teamleads

#     form = AssignProjectForm(request.POST)
    
#     teamlead = Teamlead.objects.filter(user=request.user).first()
#     data = ProjectAssignment.objects.filter(to_lead = teamlead).all()
    
#     # app2 = LeadProjectUpdate.objects.filter(id=request.POST.get('answer')).all()
#     if form.is_valid():
#         # form.instance.user = teamlead
#         form.save()
#         return redirect('teamleads')
#     # for items in app2:

#     #     items.status = request.POST.get('status')
#     #     items.save()

#     context = { 'form':form }

#     return render(request,'tAssignProject.html',context)