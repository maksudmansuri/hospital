from django.urls import path
from patient import views

urlpatterns = [  
    path('', views.patientdDashboardViews.as_view(), name="patient_home"),
    path('patient_update', views.patientdUpdateViews.as_view(), name="patient_update"),
    path('hospital_list', views.HospitalListViews.as_view(), name="hospital_list"),
    path('hospital_details/<id>', views.HospitalDetailsViews.as_view(), name="hospital_details"),
    path('bookappoinment/<id>/<did>', views.DoctorsBookAppoinmentViews.as_view(), name="bookappoinment"),
    path('bookanappointment', views.BookAnAppointmentViews.as_view(), name="bookanappointment"),
    path('labbookanappointment', views.BookAnAppointmentForLABViews.as_view(), name="labbookanappointment"),
    path('viewbookedanappointment', views.ViewBookedAnAppointmentViews.as_view(), name="viewbookedanappointment"),
    path('cancelbookedanappointment/<id>', views.CancelBookedAnAppointmentViews, name="cancelbookedanappointment"),
    path('cancellabbookedanappointment/<id>', views.CancelLabBookedAnAppointmentViews, name="cancellabbookedanappointment"),
    
    # Laboratory urls
    path('laboratory_list', views.LabListViews.as_view(), name="laboratory_list"),
    path('laboratory_details/<id>', views.labDetailsViews.as_view(), name="laboratory_details"),
    
    #checkout for lab and hospital combin 
    path('checkout', views.CheckoutViews, name="checkout"),
    path('paytmprocess', views.PaytmProcessViews, name="paytmprocess"),

    path('handlerequest', views.handlerequest, name="handlerequest"),


  
]