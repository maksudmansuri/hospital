from patient.api import views
from django.conf.urls import url
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
  
urlpatterns = [

    #Hospital's APIs 
    
    path('hospitalslist', views.ApiHospitalListAndDetailsView.as_view(),name='hospitalslist'),
    path('hospitalsdetials/<id>', views.ApiHospitalListAndDetailsView.as_view(),name='hospitalsdetials'),
    path('hospitaldoctordetail/<id>/<did>', views.HospitalDoctorDetailsView.as_view(),name='hospitaldoctordetail'),

    path('onlinedoctorlist',views.APIOnlineDoctorListView.as_view(),name='onlinedoctorlist'),
    path('onlinedoctordetail/<id>',views.APIOnlineDoctorListView.as_view(),name='onlinedoctordetail'),
   
    path('homevisitdoctorlist',views.APIHomevisitDoctorListView.as_view(),name='homevisitdoctorlist'),
    path('homevisitdetail/<id>',views.APIHomevisitDoctorListView.as_view(),name='homevisitdetail'),
    # path('doctorschedules/<id>/<did>/<sid>', views.HospitalDoctorDetailsView.as_view(),name='hospitaldoctordetail'),

    # Lab's APIs

    path('labslist', views.ApiLabsListAndDetailsView.as_view(),name='labslist'),
    path('labsdetials/<id>', views.ApiLabsListAndDetailsView.as_view(),name='labsdetials'),
 
 
    # Pharmacy's APIs

    path('pharmacylist', views.ApiPharmacyListAndDetailsView.as_view(),name='pharmacylist'),
    path('pharmacydetials/<id>', views.ApiPharmacyListAndDetailsView.as_view(),name='pharmacydetials'),


    # List Of AppointmentBooked
     path('appointmentlist', views.AppointmentListView.as_view(),name='appointmentlist'),
     path('appointmentdetail/<id>', views.AppointmentListView.as_view(),name='appointmentdetail'),

]
