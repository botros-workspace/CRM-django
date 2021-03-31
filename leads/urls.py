from django.urls import path 
from .views import lead_list, lead_detail, lead_create, lead_update, lead_delete, LeadListView, LeadDetailView, LeadUpdateView, LeadDeleteView, LeadCreateView, AssignAgentView, CategoryListView, CategoryDetailView, LeadCategoryUpdateView,LeadCategoryAdd,LeadCategoryDelete

app_name = "leads"

urlpatterns = [
    path('', LeadListView.as_view(), name = 'lead-list'),
    #We specify the typy of the PK that is expected so we don't get errors when
    #we write other String types URLS
    path('<int:pk>/', LeadDetailView.as_view(), name = 'lead-detail'),
    path('<int:pk>/update/', LeadUpdateView.as_view(), name = 'lead-update'),
    path('<int:pk>/delete/', LeadDeleteView.as_view(), name = 'lead-delete'),
    path('<int:pk>/assign-agent/', AssignAgentView.as_view(), name = 'assign-agent'),
    path('<int:pk>/category', LeadCategoryUpdateView.as_view(), name = "lead-category-update"),
    path('create/', LeadCreateView.as_view(), name = 'lead-create'),
    path('categories/', CategoryListView.as_view(), name ="category-list"),
    path('categories/<int:pk>', CategoryDetailView.as_view(), name ="category-detail"),
    path('categories/<int:pk>/delete',LeadCategoryDelete.as_view(), name= "category-delete" ),
    path('categories/add',LeadCategoryAdd.as_view(), name= "category-add" ),

]
