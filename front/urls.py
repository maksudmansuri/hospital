from django.urls import path
from .import views

urlpatterns = [  
    path('',views.FrontView.as_view(),name="front_home"),
   

 
]