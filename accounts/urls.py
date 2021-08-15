from django.urls import path
from .import views

urlpatterns = [ 
    # path('auth_404',views.auth404View,name="auth_404"), 
    # path('auth_password_reset',views.auth_password_resetView,name="auth_password_reset"), 
    # path('auth_signin',views.auth_signinView,name="auth_signin"), 
    # path('auth_signup',views.auth_signupView,name="auth_signup"), 
    # path('auth_two_step',views.auth_two_stepView,name="auth_two_step"), 
    path('dologin', views.dologin,name='dologin'),
    path('dosingup', views.adminSingup,name='dosingup'),
    path('hospitalsingup', views.HospitalSingup.as_view(),name='hospitalsingup'),
    path('doctorsingup', views.DoctorSingup.as_view(),name='doctorsingup'),
    path('patientsingup', views.PatientSingup.as_view(),name='patientsingup'),
    path('labsingup', views.LabSingup.as_view(),name='labsingup'),
    path('pharmacysingup', views.PharmacySingup.as_view(),name='pharmacysingup'),
    path('activate/<uidb64>/<token>', views.activate,name='activate'),
    
]