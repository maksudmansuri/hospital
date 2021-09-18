from django.urls import path
from .import views

urlpatterns = [ 
    path('',views.LabDashboardViews.as_view(),name="pharmacy_home"),
    path('pharmacy_update',views.PharmacyUpdateViews.as_view(),name="pharmacy_update"),
    path('view_pharmacy_appointment',views.ViewAppointmentViews.as_view(),name="view_pharmacy_appointment"),
    path('delete_pharmacy_appointment',views.deleteServicesViews,name="delete_pharmacy_appointment"),
 
]