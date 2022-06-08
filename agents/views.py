import random
from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent
from django.shortcuts import reverse
from .forms import AgentModelForm
from .mixins import OrganizorAndLoginRequiredMixin
from django.core.mail import send_mail
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
    
    # creates user then asigns user to Agent model. 
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organizor = False
        user.set_password(f"{random.randint(0,1000000)}")
        user.save()
        Agent.objects.create(
            user=user,
            organization = self.request.user.userprofile
        )
        send_mail(
            subject="You have been invied to become an Agent",
            message="You have been added as an Agent on Kalu CRM. Please log in to start working",
            from_email = "admin@test.com",
            recipient_list=[user.email]
        )
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
