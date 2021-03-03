from django.shortcuts import render, redirect, reverse
from .models import Lead
from django.views import generic
from .forms import LeadModelForm

#class based View
class LandingPageView(generic.TemplateView):
    template_name = "landing-page.html"

class LeadListView(generic.ListView):
    template_name= "lead-list.html"
    queryset= Lead.objects.all()
    context_object_name = "leads"

class LeadDetailView(generic.DetailView):
    template_name= "lead-detail.html"
    queryset= Lead.objects.all()
    context_object_name = "lead"

class LeadCreateView(generic.CreateView):
    template_name= "lead-list.html"
    form_class= LeadModelForm
    
    def get_success_url(self):
        return reverse("leads:lead-list")

class LeadUpdateView(generic.UpdateView):
    template_name= "lead-update.html"
    form_class= LeadModelForm
    queryset = Lead.objects.all()
    
    def get_success_url(self):
        return reverse("leads:lead-list")

class LeadDeleteView(generic.DeleteView):
    template_name= "lead-delete.html"
    queryset = Lead.objects.all()
   
    def get_success_url(self):
        return reverse("leads:lead-list")

#function based View
def landing_page(request):
    return render(request, "landing-page.html")

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
