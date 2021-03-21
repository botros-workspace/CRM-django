import random
from django.core.mail import send_mail
from django.shortcuts import render, reverse
from django.views import generic
from .mixins import OrganizerAndLoginRequiredMixin
from leads.models import Agent
from .forms import AgentModelForm

class AgentListView(OrganizerAndLoginRequiredMixin, generic.ListView):
    template_name = "agent-list.html"

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization =  organization)     

class AgentCreateView(OrganizerAndLoginRequiredMixin, generic.CreateView):
    template_name = "agent-create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")

    def form_valid(self, form):
        user = form.save(commit = False)
        user.is_agent = True
        user.is_organizer = False
        user.set_password(f"{random.randint(0,10000000)}")
        user.save()
        Agent.objects.create(
            user= user,
            organization= self.request.user.userprofile
        )
        send_mail(
            subject="Invetaion",
            message="Yo were added as an agent on CRM. Please come login to start working",
            from_email="admin@CRM.com",
            recipient_list=[user.email]
        )

        return super(AgentCreateView,self).form_valid(form)

class AgentDetailView(OrganizerAndLoginRequiredMixin, generic.DetailView):
    template_name = "agent-detail.html"
    
    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization = organization)

class AgentUpdateView(OrganizerAndLoginRequiredMixin, generic.UpdateView):
    template_name= "agent-update.html"
    queryset = Agent.objects.all()
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")

class AgentDeleteView(OrganizerAndLoginRequiredMixin, generic.DeleteView):
    template_name = "agent-delete.html"

    def get_success_url(self):
        return reverse("agents:agent-list")

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization = organization)