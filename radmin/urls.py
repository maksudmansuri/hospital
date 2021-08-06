from django.urls import path
from .import views

urlpatterns = [
    path('',views.indexView,name="radmin_home"), 
    path('virtual',views.virtualView,name="virtual"),
    path('doctor_all',views.doctorallView,name="doctor_all"),
    path('doctor_add',views.doctor_addView,name="doctor_add"),
    path('appoinment',views.appoinmentView,name="appoinment"),
    path('doctor_profile',views.doctorprofileView,name="doctor_profile"),
    path('doctor_schedule',views.doctorscheduleView,name="doctor_schedule"),
    path('patient_list',views.patientlistView,name="patient_list"),
    path('patient_add',views.patientaddtView,name="patient_add"),
 
    path('patient_profile',views.patientprofileView,name="patient_profile"),
    path('patient_invoice',views.patientinvoiceView,name="patient_invoice"),
 
    path('patient_profile',views.patientprofileView,name="patient_profile"),
    path('patient_invoice',views.patientinvoiceView,name="patient_invoice"),
    path('accidents',views.accidentsView,name="accidents"),
    path('labs',views.labsviews,name="labs"),
    path('department',views.departmentviews,name="department"),
    path('invoices',views.invicesviews,name="invoices"),
    path('payments',views.paymentsviews,name="payments"),
    path('expences',views.expencesviews,name="expences"),
 
]