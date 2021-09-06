from django.urls import path
from patient import views

urlpatterns = [  
    path('', views.patientdDashboardViews.as_view(), name="patient_home"),
    path('patient_update', views.patientdUpdateViews.as_view(), name="patient_update"),
    path('hospital_list', views.HospitalListViews.as_view(), name="hospital_list"),
    path('hospital_details/<id>', views.HospitalDetailsViews.as_view(), name="hospital_details"),
  
]