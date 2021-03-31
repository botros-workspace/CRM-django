from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from .models import Lead, Category
from django.views import generic
from .forms import LeadModelForm, CustomUserCreationForm, AssignAgentForm, LeadCategoryUpdateForm, CategoryModelForm
from agents.mixins import OrganizerAndLoginRequiredMixin

#class based View
class SignupView(generic.CreateView):
    template_name= "registration/signup.html"
    form_class= CustomUserCreationForm
    
    def get_success_url(self):
        return reverse("login")

class LandingPageView(generic.TemplateView):
    template_name = "landing-page.html"

class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name= "lead-list.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user

        if user.is_organizer:
            queryset = Lead.objects.filter(organization = user.userprofile, agent__isnull = False)
        else:
            queryset = Lead.objects.filter(organization = user.agent.organization, agent__isnull = False)
            queryset = queryset.filter(agent__user = user)
        return queryset

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(LeadListView, self).get_context_data(**kwargs)
        if user.is_organizer:
            queryset = Lead.objects.filter(organization = user.userprofile, agent__isnull = True)
            context.update({
                "unassigned_leads": queryset
            })
        return context
    
class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name= "lead-detail.html"
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user

        if user.is_organizer:
            queryset = Lead.objects.filter(organization = user.userprofile)
        else:
            queryset = Lead.objects.filter(organization = user.agent.organization)
            queryset = queryset.filter(agent__user = user)
        return queryset

class LeadCreateView(OrganizerAndLoginRequiredMixin, generic.CreateView):
    template_name= "lead-create.html"
    form_class= LeadModelForm
    
    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        lead = form.save(commit= False)
        lead.organization = self.request.user.userprofile
        lead.save()
        send_mail(
            subject = "A lead has been created",
            message = "Go to the site to see the new lead",
            from_email = "test@test.com",
            recipient_list = ["test2@test2.com"]
        )
        return super(LeadCreateView, self).form_valid(form)

class LeadUpdateView(OrganizerAndLoginRequiredMixin, generic.UpdateView):
    template_name= "lead-update.html"
    form_class= LeadModelForm
    
    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organization = user.userprofile)

    def get_success_url(self):
        return reverse("leads:lead-list")

class LeadDeleteView(OrganizerAndLoginRequiredMixin, generic.DeleteView):
    template_name= "lead-delete.html"
    
    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organization = user.userprofile)
   
    def get_success_url(self):
        return reverse("leads:lead-list")

class AssignAgentView(OrganizerAndLoginRequiredMixin, generic.FormView):
    template_name = "assign-agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request":self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id = self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)

class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "category-list.html"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_organizer:
            queryset = Lead.objects.filter(organization= user.userprofile)
        else:
            queryset = Lead.objects.filter(organization= user.agent.organization)

        context.update({
            "unassigned_lead_count": queryset.filter(category__isnull = True).count()
        })
        return context

    def get_queryset(self):
        user = self.request.user

        if user.is_organizer:
            queryset = Category.objects.filter(organization = user.userprofile)
        else:
            queryset = Category.objects.filter(organization = user.agent.organization)
        return queryset



class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "category-detail.html"
    context_object_name = "category"
    #use this method when you want to perform a more complex queryset, instead of rendering through the leads that belongs to that category inside of the html 
    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        if user.is_organizer:
            leads = self.get_object().leads.filter(organization = user.userprofile)
        else:
            leads = self.get_object().leads.filter(organization = user.agent.organization)
            leads = leads.filter(agent__user = user)
            
        context.update({
            "leads": leads
        })
        return context 
        
    def get_queryset(self):
        user = self.request.user

        if user.is_organizer:
            queryset = Category.objects.filter(organization = user.userprofile)
        else:
            queryset = Category.objects.filter(organization = user.agent.organization)
        return queryset

class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name= "lead-category-update.html"
    form_class= LeadCategoryUpdateForm
    
    def get_queryset(self):
        user = self.request.user

        if user.is_organizer:
            queryset = Lead.objects.filter(organization = user.userprofile)
        else:
            queryset = Lead.objects.filter(organization = user.agent.organization)
            queryset = queryset.filter(agent__user = user)
        return queryset

    def get_success_url(self):
        return reverse("leads:lead-list")
        # return reverse("leads:lead-detail", kwargs={"pk": self.get_object().id})

class LeadCategoryAdd(OrganizerAndLoginRequiredMixin, generic.CreateView):
    template_name= "category-add.html"
    form_class= CategoryModelForm
    
    def get_success_url(self):
        return reverse("leads:category-list")

    def form_valid(self, form):
        category = form.save(commit= False)
        category.organization = self.request.user.userprofile
        category.save()
        return super(LeadCategoryAdd, self).form_valid(form)

class LeadCategoryDelete(OrganizerAndLoginRequiredMixin, generic.DeleteView):
    template_name= "category-delete.html"
  
    def get_queryset(self):
        user = self.request.user
        return Category.objects.filter(organization = user.userprofile)
        
    def get_success_url(self):
        return reverse("leads:category-list")

#function based View
def landing_page(request):
    return render(request, "landing-page.html", )

def lead_list(request):
    leads = Lead.objects.all()
    context = {
        'leads': leads
    }
    return render(request,"lead-list.html", context = context)

def lead_detail(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        'lead' : lead
    }
    return render(request, "lead-detail.html", context = context)

def lead_create(request):
    form = LeadModelForm()
    if request.method =="POST":
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/leads")
    context = {
        'form' : form
    }
    return render(request, "lead-create.html", context = context)

def lead_update(request,pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance = lead)
    if request.method =="POST":
        form = LeadModelForm(request.POST, instance= lead)
        if form.is_valid():
            form.save()
            return redirect("/leads/"+str(pk))
    context = {
        'form' : form,
        'lead' : lead
    }
    return render(request, "lead-update.html", context = context)

def lead_delete(request, pk):
    lead = Lead.objects.get(id= pk)
    lead.delete()
    return redirect("/leads")
