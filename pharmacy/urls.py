from django.urls import path
from .import views

urlpatterns = [  
    path('',views.LabDashboardViews.as_view(),name="pharmacy_home"),
    path('pharmacy_update',views.PharmacyUpdateViews.as_view(),name="pharmacy_update"),
    path('view_pharmacy_appointment',views.ViewPharmacyAppointmentViews.as_view(),name="view_pharmacy_appointment"),
    path('updload_invoice_pharmacy/<id>',views.UpdloadInvoicePharmacy,name="updload_invoice_pharmacy"),
    path('pharmacy_manage_gallery',views.ViewImageViews.as_view(),name="pharmacy_manage_gallery"),
    path('delete_pharmacy_appointment/<id>',views.deleteServicesViews,name="delete_pharmacy_appointment"),
 
]