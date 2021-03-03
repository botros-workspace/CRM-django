from django.urls import path 
from .views import lead_list, lead_detail, lead_create

app_name = "leads"

urlpatterns = [
    path('', lead_list),
    #We specify the typy of the PK that is expected so we don't get errors when
    #we write other String types URLS
    path('<int:pk>/', lead_detail),
    path('create/', lead_create),
]
