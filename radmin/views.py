from patient.models import Booking, LabTest, Orders, Slot
from django.core.files.storage import FileSystemStorage
from django.http.response import HttpResponseRedirect
from hospital.models import ContactPerson, HospitalMedias, HospitalStaffDoctorSchedual, HospitalStaffDoctors, Insurances, ServiceAndCharges
from accounts.models import CustomUser, HospitalPhones, Hospitals, Labs, Patients, Pharmacy
from django.shortcuts import get_object_or_404, render
from django.views.generic import View,CreateView,DetailView,DeleteView,ListView,UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.db.models import Q
# Create your views here.
   
def indexView(request):
       
    return render(request,"radmin/index.html")
 
 
"""
Hospitals All Views
"""

class HospitalallViews(ListView):
    model = Hospitals
    template_name = "radmin/hospital_all.html" 

def HospitalActivate(request,id):
    hospital=Hospitals.objects.get(id=id)
    if hospital is not None and hospital.is_verified == False:
        hospital.is_verified=True
        hospital.is_appiled=False
        hospital.is_deactive=False
        hospital.save()
    # hospitals_list=Hospitals.objects.filter((Q(is_appiled=True) | Q(is_verified=True))  & Q(admin__is_active=True) & Q(admin__user_type=3))
    return HttpResponseRedirect(reverse("manage_hospital_admin"))

def HospitalDeactivate(request,id):
    hospital=Hospitals.objects.get(id=id)
    if hospital is not None and hospital.is_verified == True:
        hospital.is_verified=False
        hospital.is_appiled=False
        hospital.is_deactive=True
        hospital.save()
    return HttpResponseRedirect(reverse("manage_hospital_admin"))
    # return render(request,'counsellor/manage_student.html',{'hospitals_list':hospitals_list})

def HospitalDelete(request,id):
    hospital=Hospitals.objects.get(id=id)
    hospital.delete()
    return HttpResponseRedirect(reverse("manage_hospital_admin"))


"""
Patients All Views
"""

class PatientAllViews(ListView):
    model = Patients
    template_name = "radmin/patient_all.html" 

def PatientActivate(request,id):
    hospital=Patients.objects.get(id=id)
    if hospital is not None and hospital.is_verified == False:
        hospital.is_verified=True
        hospital.is_appiled=False
        hospital.is_deactive=False
        hospital.save()
    # hospitals_list=Hospitals.objects.filter((Q(is_appiled=True) | Q(is_verified=True))  & Q(admin__is_active=True) & Q(admin__user_type=3))
    return HttpResponseRedirect(reverse("manage_patient_admin"))

def PatientDeactivate(request,id):
    hospital=Patients.objects.get(id=id)
    if hospital is not None and hospital.is_verified == True:
        hospital.is_verified=False
        hospital.is_appiled=False
        hospital.is_deactive=True
        hospital.save()
    return HttpResponseRedirect(reverse("manage_patient_admin"))
    # return render(request,'counsellor/manage_student.html',{'hospitals_list':hospitals_list})

def PatientDelete(request,id):
    hospital=Patients.objects.get(id=id)
    hospital.delete()
    return HttpResponseRedirect(reverse("manage_patient_admin"))


"""
Labs All Views
"""

class LabsAllViews(ListView):
    model = Labs
    template_name = "radmin/laboratory_all.html" 

def LabsActivate(request,id):
    hospital=Labs.objects.get(id=id)
    if hospital is not None and hospital.is_verified == False:
        hospital.is_verified=True
        hospital.is_appiled=False
        hospital.is_deactive=False
        hospital.save()
    # hospitals_list=Hospitals.objects.filter((Q(is_appiled=True) | Q(is_verified=True))  & Q(admin__is_active=True) & Q(admin__user_type=3))
    return HttpResponseRedirect(reverse("manage_labs_admin"))

def LabsDeactivate(request,id):
    hospital=Labs.objects.get(id=id)
    if hospital is not None and hospital.is_verified == True:
        hospital.is_verified=False
        hospital.is_appiled=False
        hospital.is_deactive=True
        hospital.save()
    return HttpResponseRedirect(reverse("manage_labs_admin"))
    # return render(request,'counsellor/manage_student.html',{'hospitals_list':hospitals_list})

def LabsDelete(request,id):
    hospital=Labs.objects.get(id=id)
    hospital.delete()
    return HttpResponseRedirect(reverse("manage_labs_admin"))

"""
Pharmacy All Views
"""

class PharmacyAllViews(ListView):
    model = Pharmacy
    template_name = "radmin/pharmacy_all.html" 

def PharmacyActivate(request,id):
    hospital=Hospitals.objects.get(id=id)
    if hospital is not None and hospital.is_verified == False:
        hospital.is_verified=True
        hospital.is_appiled=False
        hospital.is_deactive=False
        hospital.save()
    # hospitals_list=Hospitals.objects.filter((Q(is_appiled=True) | Q(is_verified=True))  & Q(admin__is_active=True) & Q(admin__user_type=3))
    return HttpResponseRedirect(reverse("manage_pharmacy_admin"))

def PharmacyDeactivate(request,id):
    hospital=Hospitals.objects.get(id=id)
    if hospital is not None and hospital.is_verified == True:
        hospital.is_verified=False
        hospital.is_appiled=False
        hospital.is_deactive=True
        hospital.save()
    return HttpResponseRedirect(reverse("manage_pharmacy_admin"))
    # return render(request,'counsellor/manage_student.html',{'hospitals_list':hospitals_list})

def PharmacyDelete(request,id):
    hospital=Hospitals.objects.get(id=id)
    hospital.delete()
    return HttpResponseRedirect(reverse("manage_pharmacy_admin"))


"""
Accident All Views
"""

class AccidentAllViews(ListView):
    model = Hospitals
    template_name = "radmin/accident_all.html" 

def AccidentActivate(request,id):
    hospital=Hospitals.objects.get(id=id)
    if hospital is not None and hospital.is_verified == False:
        hospital.is_verified=True
        hospital.is_appiled=False
        hospital.is_deactive=False
        hospital.save()
    # hospitals_list=Hospitals.objects.filter((Q(is_appiled=True) | Q(is_verified=True))  & Q(admin__is_active=True) & Q(admin__user_type=3))
    return HttpResponseRedirect(reverse("manage_accident_admin"))

def AccidentDeactivate(request,id):
    hospital=Hospitals.objects.get(id=id)
    if hospital is not None and hospital.is_verified == True:
        hospital.is_verified=False
        hospital.is_appiled=False
        hospital.is_deactive=True
        hospital.save()
    return HttpResponseRedirect(reverse("manage_accident_admin"))
    # return render(request,'counsellor/manage_student.html',{'hospitals_list':hospitals_list})

def AccidentDelete(request,id):
    hospital=Hospitals.objects.get(id=id)
    hospital.delete()
    return HttpResponseRedirect(reverse("manage_accident_admin"))


def hospitalUpdateView(request): 
    return render(request,"radmin/doctor_add.html")
 
def hospitalDeleteView(request): 
    return render(request,"radmin/doctor_add.html")

"""
Appointment all view
"""
class HosAppointmentAllViews(ListView):
    model = Booking
    template_name = "radmin/appointment_hospital_all.html" 

class LabsAppointmentAllViews(ListView):
    def get(self, request, *args, **kwargs):
        allslot = Slot.objects.filter(is_active=True)
        allslot_list = []
        for slots in allslot:
            labtest = LabTest.objects.filter(slot=slots)
            allslot_list.append({'slot':slots,'labtest':labtest})
        param = {'allslot_list':allslot_list}
        return render(request,"radmin/appointment_labs_all.html",param)

"""
Profile of Hospital Labs Pharmacy Patient
"""
class HospitalDetailsViews(DetailView):
    def get(self, request, *args, **kwargs):
        hosital_id=kwargs['id']
        hospital = get_object_or_404(Hospitals,admin__is_active=True,is_verified=True,is_deactive=False,id=hosital_id)
        doctors = HospitalStaffDoctors.objects.filter(is_active=True,hospital=hospital)
        hospitalservice = ServiceAndCharges.objects.filter(user=hospital.admin)
        hospitalstaffdoctor_list = []
        for hospitalstaffdoctor in doctors:
            hospitalstaffdoctorschedual = HospitalStaffDoctorSchedual.objects.filter(hospitalstaffdoctor=hospitalstaffdoctor)
            opd_time = []
            for dcsh in hospitalstaffdoctorschedual:
                if dcsh.work == "OPD":
                    shift = dcsh.shift
                    start_time = dcsh.start_time
                    end_time = dcsh.end_time
                opd_time.append({'shift':shift,'start_time':start_time,'end_time':end_time})
            hospitalstaffdoctor_list.append({'hospitalstaffdoctor':hospitalstaffdoctor,'hospitalstaffdoctorschedual':hospitalstaffdoctorschedual,'opd_time':opd_time})
        param = {'hospital':hospital,'hospitalstaffdoctor_list':hospitalstaffdoctor_list,'hospitalservice':hospitalservice}  
        return render(request,"radmin/hospital_profile.html",param)

class DoctorsBookAppoinmentViews(SuccessMessageMixin,View):
    def get(self, request, *args, **kwargs):
        hosital_id=kwargs['id']
        hositaldcotorid_id=kwargs['did']
        hospital = get_object_or_404(Hospitals,is_verified=True,is_deactive=False,id=hosital_id)
        hospitalstaffdoctor = get_object_or_404(HospitalStaffDoctors,is_active=True,id=hositaldcotorid_id)
        hospitalservice = ServiceAndCharges.objects.filter(user=hospital.admin)
      
        
        hospitalstaffdoctorschedual =HospitalStaffDoctorSchedual.objects.filter(hospitalstaffdoctor=hospitalstaffdoctor)
        opd_time = []
        for dcsh in hospitalstaffdoctorschedual:
            if dcsh.work == "OPD":
                shift = dcsh.shift
                start_time = dcsh.start_time
                end_time = dcsh.end_time
            opd_time.append({'shift':shift,'start_time':start_time,'end_time':end_time})
        
        param = {'hospital':hospital,'hospitalservice':hospitalservice,'hospitalstaffdoctor':hospitalstaffdoctor,'hospitalstaffdoctorschedual':hospitalstaffdoctorschedual,'opd_time':opd_time}  
        return render(request,"radmin/doctor_profile.html",param)
    
class LabDetailsViews(DetailView):
    def get(self, request, *args, **kwargs):
        lab_id=kwargs['id']
        lab = get_object_or_404(Labs,admin__is_active=True,is_verified=True,is_deactive=False,id=lab_id)
        services = ServiceAndCharges.objects.filter(user=lab.admin)        
        param = {'lab':lab,'services':services}  
        return render(request,"radmin/lab_profile.html",param)

class PharmacyDetailsViews(DetailView):
    def get(self, request, *args, **kwargs):
        lab_id=kwargs['id']
        pharmacy = get_object_or_404(Pharmacy,admin__is_active=True,is_verified=True,is_deactive=False,id=lab_id)   

        param = {'pharmacy':pharmacy}  
        return render(request,"radmin/pharmacy_profile.html",param)

class PatientDetailsViews(DetailView):
    def get(self, request, *args, **kwargs):
        patient_id=kwargs['id']
        patient = get_object_or_404(Patients,admin__is_active=True,id=patient_id)
        slotbook = Slot.objects.filter(patient=patient.admin)
        allslot_list = []
        for slots in slotbook:
            labtests = LabTest.objects.filter(slot=slots)
            allslot_list.append({'slot':slots,'labtests':labtests})
        booking = Booking.objects.filter(patient=patient.admin) 

        param = {'patient':patient,'allslot_list':allslot_list,'booking':booking}  
        return render(request,"radmin/patient_profile.html",param)

