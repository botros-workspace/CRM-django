from django.urls import path 
from .views import lead_list, lead_detail, lead_create, lead_update, lead_delete

app_name = "leads"

urlpatterns = [
    path('', lead_list),
    #We specify the typy of the PK that is expected so we don't get errors when
    #we write other String types URLS
    path('<int:pk>/', lead_detail),
    path('<int:pk>/update/', lead_update),
    path('<int:pk>/delete/', lead_delete),
    path('create/', lead_create),
]
