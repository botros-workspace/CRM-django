from django.shortcuts import render, reverse
from django.views import generic
from .mixins import OrganizerAndLoginRequiredMixin
from leads.models import Agent
from .forms import AgentModelForm

class AgentListView(OrganizerAndLoginRequiredMixin, generic.ListView):
    template_name = "agent-list.html"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation = organisation)

class AgentCreateView(OrganizerAndLoginRequiredMixin, generic.CreateView):
    template_name = "agent-create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")

    def form_valid(self, form):
        agent = form.save(commit = False)
        agent.organisation = self.request.user.userprofile
        agent.save()

        return super(AgentCreateView,self).form_valid(form)

class AgentDetailView(OrganizerAndLoginRequiredMixin, generic.DetailView):
    template_name = "agent-detail.html"
    
    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation = organisation)

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
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation = organisation)