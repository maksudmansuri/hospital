from django.shortcuts import render
from django.views.generic import View
# Create your views here.
 
def indexView(request): 
    return render(request,"radmin/index.html")

def virtualView(request): 
    return render(request,"radmin/virtual.html")

def doctorallView(request): 
    return render(request,"radmin/doctor_all.html")

def doctor_addView(request): 
    return render(request,"radmin/doctor_add.html")

def appoinmentView(request): 
    return render(request,"radmin/appoinment.html")

def doctorprofileView(request): 
    return render(request,"radmin/doctor_profile.html")

def doctorscheduleView(request): 
    return render(request,"radmin/doctor_schedule.html")
    
def patientlistView(request): 
    return render(request,"radmin/patient_list.html")

def patientaddtView(request): 
    return render(request,"radmin/patient_add.html")
    
def patientprofileView(request): 
    return render(request,"radmin/patient_profile.html")
    
def patientinvoiceView(request): 
    return render(request,"radmin/patient_invoice.html")

def accidentsView(request): 
    return render(request,"radmin/accidents.html")

def labsviews(request): 
    return render(request,"radmin/labs.html")

def departmentviews(request): 
    return render(request,"radmin/department.html")
 
def invicesviews(request): 
    return render(request,"radmin/invoices.html") 
 
def paymentsviews(request): 
    return render(request,"radmin/payments.html")
 
def expencesviews(request): 
    return render(request,"radmin/expences.html")

 