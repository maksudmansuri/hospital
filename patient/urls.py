from django.urls import path,re_path
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
    path('CancelPictureForMedicineViews/<id>', views.CancelPictureForMedicineViews, name="CancelPictureForMedicineViews"),
    
    # Laboratory urls
    path('laboratory_list', views.LabListViews.as_view(), name="laboratory_list"),
    path('laboratory_details/<id>', views.labDetailsViews.as_view(), name="laboratory_details"),
    path('send_to_doctor/<id>', views.ReportSendToDoctorViews, name="send_to_doctor"),
    #Pharmacy urls
    path('pharmacy_list', views.PharmacyListViews.as_view(), name="pharmacy_list"),
    path('pharmacy_details/<id>', views.PharmacyDetailsViews.as_view(), name="pharmacy_details"),
    path('updload_prescription_photo', views.UploadPresPhotoViews.as_view(), name="updload_prescription_photo"),

    #checkout for lab and hospital combin 
    path('checkout', views.CheckoutViews, name="checkout"),
    path('payformedicine/<id>', views.PayForMedicine, name="payformedicine"),
    path('paytmprocess', views.PaytmProcessViews, name="paytmprocess"),

    path('handlerequest', views.handlerequest, name="handlerequest"),

    # Virtual patient
    path('list_of_virtual_doctor', views.ListofVirtualDoctor, name="list_of_virtual_doctor"),
    
    
    # Home Visit patient
    path('home_visit_doctor/<id>/<did>', views.HomeVisitDoctor.as_view(), name="home_visit_doctor"),
    path('bookanappointmentforhomevisit', views.BookanAppointmentForHomeVisit, name="bookanappointmentforhomevisit"),

    # add Some one as petient add , update , delete
    path('add_someone_as_patient', views.AddSomeoneAsPatient, name="add_someone_as_patient"),

    path('<booking_id>',views.bookingConfirmation,name="booking_confirmation"),
    path('lab/<slot_id>',views.slotConfirmation,name="lab_confirmation"),
    path('pharmacy/<booking_id>',views.picturesformedicineConfirmation,name="pharmacy_confirmation"),


    

]