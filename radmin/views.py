from django.core.files.storage import FileSystemStorage
from django.http.response import HttpResponseRedirect
from hospital.models import ContactPerson, HospitalMedias, Insurances
from accounts.models import CustomUser, HospitalPhones, Hospitals
from django.shortcuts import render
from django.views.generic import View,CreateView,DetailView,DeleteView,ListView,UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.db.models import Q
# Create your views here.
   
def indexView(request):  
    return render(request,"radmin/index.html")
 
class hospitalallViews(ListView):
    model = Hospitals
    template_name = "radmin/hospital_all.html" 
    

def hospitalActivate(request,id):
    hospital=Hospitals.objects.get(id=id)
    if hospital is not None and hospital.is_verified == False:
        hospital.is_verified=True
        hospital.is_appiled=False
        hospital.is_deactive=False
        hospital.save()
    # hospitals_list=Hospitals.objects.filter((Q(is_appiled=True) | Q(is_verified=True))  & Q(admin__is_active=True) & Q(admin__user_type=3))
    return HttpResponseRedirect(reverse("manage_hospital"))

def hospitalDeactivate(request,id):
    hospital=Hospitals.objects.get(id=id)
    if hospital is not None and hospital.is_verified == True:
        hospital.is_verified=False
        hospital.is_appiled=False
        hospital.is_deactive=True
        hospital.save()
    return HttpResponseRedirect(reverse("manage_hospital"))
    # return render(request,'counsellor/manage_student.html',{'hospitals_list':hospitals_list})

def hospitalDelete(request,id):
    hospital=Hospitals.objects.get(id=id)
    hospital.delete()
    return HttpResponseRedirect(reverse("manage_hospital"))

def hospitalUpdateView(request): 
    return render(request,"radmin/doctor_add.html")
 
def hospitalDeleteView(request): 
    return render(request,"radmin/doctor_add.html")


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

 