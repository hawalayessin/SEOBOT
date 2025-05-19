from django.urls import path
from . import views

urlpatterns=[
    path('addPage/', views.addPage, name='addPage'),
   
]