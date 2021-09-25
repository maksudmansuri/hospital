from django.urls import path
from .import views
  
urlpatterns = [  
    path('',views.indexView,name="radmin_home"),
    path('admin_hospital_all',views.HospitalallViews.as_view(),name="manage_hospital_admin"),
    path('hospital_delete_admin/<id>',views.HospitalDelete,name="hospital_delete_admin"),
    path('manage_patient_admin',views.PatientAllViews.as_view(),name="manage_patient_admin"),
    path('patient_delete_admin/<id>',views.PatientDelete,name="patient_delete_admin"),
    path('manage_labs_admin',views.LabsAllViews.as_view(),name="manage_labs_admin"),
    path('labs_delete_admin/<id>',views.LabsDelete,name="labs_delete_admin"),
    path('manage_pharmacy_admin',views.PharmacyAllViews.as_view(),name="manage_pharmacy_admin"),
    path('pharmacy_delete_admin/<id>',views.PharmacyDelete,name="pharmacy_delete_admin"),
    path('manage_accident_admin',views.AccidentAllViews.as_view(),name="manage_accident_admin"),
    path('accident_delete_admin/<id>',views.AccidentDelete,name="accident_delete_admin"),
    # Appointment Hospital Labs Pharmcy  Accident
    path('hospital_appointment_admin',views.HosAppointmentAllViews.as_view(),name="hospital_appointment_admin"),
    path('labs_appointment_admin',views.LabsAppointmentAllViews.as_view(),name="labs_appointment_admin"),

    #Profiel for Hospital, Labs , Pharmcy, Patient 
    path('hospital_profile_admin/<id>',views.HospitalDetailsViews.as_view(),name="hospital_profile_admin"),
    path('doctor_profile_admin/<id>/<did>',views.DoctorsBookAppoinmentViews.as_view(),name="doctor_profile_admin"),
    path('labs_profile_admin/<id>',views.LabDetailsViews.as_view(),name="labs_profile_admin"),
    path('pharmacy_profile_admin/<id>',views.PharmacyDetailsViews.as_view(),name="pharmacy_profile_admin"),
    path('patient_profile_admin/<id>',views.PatientDetailsViews.as_view(),name="patient_profile_admin"),
   
 
    # ACTIVATE DEACTIVATE HOSPITAL, DOCTOR, PATIENT, LABS, PHARMACY ,ACCIDENT
    path('hospitalactivate/<id>',views.HospitalActivate,name="hospitalactivate"),
    path('hospitaldeactivate/<id>',views.HospitalDeactivate,name="hospitaldeactivate"),
    path('patientactivate/<id>',views.PatientActivate,name="patientactivate"),
    path('patinetdeactivate/<id>',views.PatientDeactivate,name="patinetdeactivate"),
    path('pharmacyactivate/<id>',views.PharmacyActivate,name="pharmacyactivate"),
    path('pharmacydeactivate/<id>',views.PharmacyDeactivate,name="pharmacydeactivate"),
    path('labsactivate/<id>',views.LabsActivate,name="labsactivate"),
    path('labsdeactivate/<id>',views.LabsDeactivate,name="labsdeactivate"),
    path('accidentactivate/<id>',views.AccidentActivate,name="accidentactivate"),
    path('accidentdeactivate/<id>',views.AccidentDeactivate,name="accidentdeactivate"),


]