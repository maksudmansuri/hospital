from django.urls import path
from patient import views

urlpatterns = [ 
    path('', views.patientdDashboardViews.as_view(), name="patient_home"),
    path('patient_update', views.patientdUpdateViews.as_view(), name="patient_update")
  
]