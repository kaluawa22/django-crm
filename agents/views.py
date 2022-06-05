from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent
from django.shortcuts import reverse
from .forms import AgentModelForm
from .mixins import OrganizorAndLoginRequiredMixin
# Create your views here.


class AgentListView(OrganizorAndLoginRequiredMixin, ListView):
    template_name = "agents/agent_list.html"


    def get_queryset(self):
        request_user_organization = self.request.user.userprofile
        return Agent.objects.filter(organization = request_user_organization)



class AgentCreateView(OrganizorAndLoginRequiredMixin, CreateView):
    template_name = "agents/agent_create.html"

    form_class = AgentModelForm

    def get_success_url(self):
        # returning to the list of agents url on sucess of creating new Agent. 
        return reverse("agents:agent-list")
    
    def form_valid(self, form):
        agent = form.save(commit=False)
        agent.organization = self.request.user.userprofile
        agent.save()
        return super(AgentCreateView, self).form_valid(form)



class AgentDetailView(OrganizorAndLoginRequiredMixin, DetailView):
    template_name = "agents/agent_detail.html"
    context_object_name = "agent"
    
    def get_queryset(self):
        request_user_organization = self.request.user.userprofile
        return Agent.objects.filter(organization = request_user_organization)

        
class AgentUpdateView(OrganizorAndLoginRequiredMixin, UpdateView):
    template_name = "agents/agent_update.html"

    form_class = AgentModelForm

    def get_success_url(self):
        # returning to the list of agents url on sucess of creating new Agent. 
        return reverse("agents:agent-list")
    
    def get_queryset(self):
        request_user_organization = self.request.user.userprofile
        return Agent.objects.filter(organization = request_user_organization)


class AgentDeleteView(OrganizorAndLoginRequiredMixin, DeleteView):
    template_name = "agents/agent_delete.html"
    context_object_name = "agent"
    

    def get_queryset(self):
        request_user_organization = self.request.user.userprofile
        return Agent.objects.filter(organization = request_user_organization)

    def get_success_url(self):
        return reverse("agents:agent-list")