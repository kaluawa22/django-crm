from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from .models import Lead, Agent, Category
from .forms import LeadModelForm, LeadForm, CustumUserRegisterForm, AssignAgentForm, LeadCategoryUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganizorAndLoginRequiredMixin

#CRUD+L 




class SignupView(CreateView):
    template_name = "registration/signup.html"
    form_class = CustumUserRegisterForm

    def get_success_url(self):
        return reverse("login")


class LandingPageView(TemplateView):
    template_name = "landing.html"

# Lead List Class Based View with LoginRequiredMixin
class LeadListView(LoginRequiredMixin, ListView):
    template_name = "leads/leads_list.html"
    context_object_name = "leads"
    # queryset = Lead.objects.filter()
    
    def get_queryset(self):
        # saving user object in variable to work with it
        user = self.request.user

        if user.is_organizor:
            # filtering based on if the user is an organizor 
            queryset = Lead.objects.filter(
                organization=user.userprofile, 
                agent__isnull=False
            )
         # filtering based on if the user is an Agent
        
        else:
            queryset = Lead.objects.filter(
                organization=user.agent.organization, 
                agent__isnull=False
                )
            # filter for the agnet that is logged in. 
            queryset = Lead.objects.filter(agent__user=user)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organizor:
            # filtering based on if the user is an organizor 
            queryset = Lead.objects.filter(
                organization=user.userprofile, 
                agent__isnull=True
            )
            
            context.update({
                "unassigned_leads": queryset
            })
        return context

class LeadDetailView(LoginRequiredMixin, DetailView):
    template_name = "leads/lead_detail.html"
    context_object_name = "lead"
    def get_queryset(self):
        # saving user object in variable to work with it
        user = self.request.user

        if user.is_organizor:
            # filtering based on if the user is an organizor 
            queryset = Lead.objects.filter(organization=user.userprofile)
         # filtering based on if the user is an Agent
        
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            # filter for the agnet that is logged in. 
            queryset = Lead.objects.filter(agent__user=user)
        return queryset

class LeadCreateView(OrganizorAndLoginRequiredMixin, CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")
    # adding to default form valid function. This is to send and email after the creation of a new lead. 
    def form_valid(self, form):
        # TODO send email
        send_mail(
            subject="A lead has been created", 
            message="Go to the site to see the new lead", 
            from_email="test@test.com",
            recipient_list=["test2@test2.com"]
        )
        return super(LeadCreateView, self).form_valid(form)

class LeadUpdateView(OrganizorAndLoginRequiredMixin, UpdateView):
    template_name = "leads/lead_update.html"
    form_class = LeadModelForm
    def get_queryset(self):
        # saving user object in variable to work with it
        user = self.request.user
        return Lead.objects.filter(organization=user.userprofile)
    
    def get_success_url(self):
        return reverse("leads:lead-update")

class LeadDeleteView(OrganizorAndLoginRequiredMixin, DeleteView):
    template_name = "leads/lead_delete.html"
    
    
    def get_queryset(self):
        # saving user object in variable to work with it
        user = self.request.user
        return Lead.objects.filter(organization=user.userprofile)

    def get_success_url(self):
        return reverse("leads:lead-list")

# class based view to Assign Agents 
class AssignAgentView(OrganizorAndLoginRequiredMixin, FormView):
    template_name="leads/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update ({
            "request": self.request

        })
        return kwargs

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)



class CategoryListView(LoginRequiredMixin, ListView):
    template_name = "leads/category_list"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(CategoryListView, self).get_context_data(**kwargs)
        
        if user.is_organizor:
            # filtering based on if the user is an organizor 
            queryset = Lead.objects.filter(
                organization=user.userprofile
            )
         # filtering based on if the user is an Agent
        
        else:
            queryset = Lead.objects.filter(
                organization=user.agent.organization
                )

        context.update({
            "unassigned_lead_count": Lead.objects.filter(category__isnull=True).count()
        })
        return context

    def get_queryset(self):
        # saving user object in variable to work with it
        user = self.request.user

        if user.is_organizor:
            # filtering based on if the user is an organizor 
            queryset = Category.objects.filter(
                organization=user.userprofile
            )
         # filtering based on if the user is an Agent
        
        else:
            queryset = Category.objects.filter(
                organization=user.agent.organization
                )
        return queryset


class CategoryDetailView(LoginRequiredMixin, DetailView):
    template_name = "leads/category_detail.html"
    context_object_name = "category"

    # def get_context_data(self, **kwargs):
    #     context = super(CategoryDetailView, self).get_context_data(**kwargs)
    #     leads = self.get_object().leads.all()
    #     context.update({
    #         "leads": leads
    #     })
    #     return context

    def get_queryset(self):
        # saving user object in variable to work with it
        user = self.request.user

        if user.is_organizor:
            # filtering based on if the user is an organizor 
            queryset = Category.objects.filter(
                organization=user.userprofile
            )
         # filtering based on if the user is an Agent
        
        else:
            queryset = Category.objects.filter(
                organization=user.agent.organization
                )
        return queryset


class LeadCategoryUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "leads/lead_category_update.html"
    form_class = LeadCategoryUpdateForm
    
    
    
    def get_queryset(self):
        # saving user object in variable to work with it
        user = self.request.user

        if user.is_organizor:
            # filtering based on if the user is an organizor 
            queryset = Lead.objects.filter(organization=user.userprofile)
         # filtering based on if the user is an Agent
        
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            # filter for the agent that is logged in. 
            queryset = Lead.objects.filter(agent__user=user)
        return queryset
    
    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.get_object().id})































def landing_page(request):
    return render(request, "landing.html")



def lead_list(request):
    # return render(request, "leads/home_page.html")
    leads = Lead.objects.all()

    context = {
        "leads": leads
    }
    return render(request, "leads/leads_list.html" , context)

def leads_detail(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        "lead": lead
    }
    return render(request, "leads/lead_detail.html" , context)

def lead_create(request):
    form = LeadModelForm()
    if request.method == "POST":
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/leads")
    context = {
        "form": form
    }
    return render(request, "leads/lead_create.html", context)




def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)
    if request.method == "POST":
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect("/leads")
    context = {
        "form": form,
        "lead": lead
    }
    return render(request, "leads/lead_update.html", context)


def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/leads")



# def lead_update(request, pk):
#     lead = Lead.objects.get(id=pk)
#     form = LeadForm()
#     if request.method == "POST":
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             agent = Agent.objects.first()
#             lead.first_name = first_name
#             lead.last_name = last_name
#             lead.age = age
#             lead.save()

#             return redirect("/leads")

#     context = {
#         "form": form,
#         "lead": lead
#     }
    
#     return render(request, "leads/lead_update.html", context)






    # def lead_create(request):
    # form = LeadForm()
    # if request.method == "POST":
    #     form = LeadForm(request.POST)
    #     if form.is_valid():
    #         first_name = form.cleaned_data['first_name']
    #         last_name = form.cleaned_data['last_name']
    #         age = form.cleaned_data['age']
    #         agent = Agent.objects.first()
    #         Lead.objects.create(
    #             first_name=first_name,
    #             last_name=last_name,
    #             age=age,
    #             agent=agent
    #         )
    #         return redirect("/leads")
    # context = {
    #     "form": form
    # }
    # return render(request, "leads/lead_create.html", context)