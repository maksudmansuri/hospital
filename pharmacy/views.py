from django.contrib.auth.models import User
from patient.models import PicturesForMedicine
from django.core.files.storage import FileSystemStorage
import pharmacy
from django.http.response import HttpResponse, HttpResponseRedirect
from accounts.models import OPDTime, Pharmacy
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, render
from django.views.generic.base import View
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.urls import reverse
from django.contrib import messages
from datetime import datetime
import pytz
IST = pytz.timezone('Asia/Kolkata')
# Create your views here.


class LabDashboardViews(SuccessMessageMixin,ListView):
    def get(self, request, *args, **kwargs):
      
            # hospital = Hospitals.objects.get(admin=request.user.id)
            # contacts = HospitalPhones.objects.filter(hospital=hospital)
            # insurances = Insurances.objects.filter(hospital=hospital)

            # if hospital.hopital_name and hospital.about and hospital.address1 and hospital.city and hospital.pin_code and hospital.state and hospital.country and hospital.landline and hospital.registration_proof and hospital.profile_pic and hospital.establishment_year and hospital.registration_number and hospital.alternate_mobile and contacts:
                return render(request,"pharmacy/index.html")
            
            
            # messages.add_message(request,messages.ERROR,"Some detail still Missing !")
            # param={'hospital':hospital,'insurances':insurances,'contacts':contacts}
            # return render(request,"hospital/hospital_update.html",param)
       
    # def get(self,request):
    #     print("hello in m  in lab")
    #     return render(request,"lab/index.html")

class PharmacyUpdateViews(SuccessMessageMixin,UpdateView):
    def get(self, request, *args, **kwargs):
        # hospital = None
        # # contacts = None
        # # insurances = None
        # try:
        pharmacy = Pharmacy.objects.get(admin=request.user.id)
        opdtime=OPDTime.objects.get(user=request.user)
            # insurances = Insurances.objects.filter(hospital=hospital)
        # except Exception as e:
        #     return HttpResponse(e)
        param={'pharmacy':pharmacy,'opdtime':opdtime}
        return render(request,"pharmacy/pharmacy_update.html",param) 
    
    def post(self, request, *args, **kwargs):
        pharmacy_name = request.POST.get("pharmacy_name")
        specialist = request.POST.get("specialist")
        profile_pic = request.FILES.get("profile_pic")

        about = request.POST.get("about")
        address = request.POST.get("address")
        city = request.POST.get("city")
        pin_code = request.POST.get("pin_code")
        state = "Gujarat"
        country = "India"
        landline = request.POST.get("landline")
        establishment_year = request.POST.get("establishment_year")
        registration_number = request.POST.get("registration_number")
        registration_proof = request.FILES.get("registration_proof")
        facebook = request.POST.get("facebook")
        instagram = request.POST.get("instagram")
        linkedin = request.POST.get("linkedin")
        twitter = request.POST.get("twitter")
        website = request.POST.get("website")
        # user creation Data
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        # mobile = request.POST.get("phone")
        alternate_mobile = request.POST.get("alternate_mobile")
        # email = request.POST.get("email")
        name_title = request.POST.get("name_title")

        #Schedule for hospital OPD and Appointment
        
        Sunday = request.POST.get("Sunday")
        Monday = request.POST.get("Monday")
        Tuesday = request.POST.get("Tuesday")
        Wednesday = request.POST.get("Wednesday")
        Thursday = request.POST.get("Thursday")
        Friday = request.POST.get("Friday")
        Saturday = request.POST.get("Saturday")
        Sunday = request.POST.get("Sunday")
        opening_time1 = request.POST.get("opening_time")
        opening_time = datetime.strptime(opening_time1,"%H:%M").time()
        close_time1 = request.POST.get("close_time")
        close_time = datetime.strptime(close_time1,"%H:%M").time()
        break_start_time1 = request.POST.get("break_start_time")
        break_start_time = datetime.strptime(break_start_time1,"%H:%M").time()
        break_end_time1 = request.POST.get("break_end_time")
        break_end_time = datetime.strptime(break_end_time1,"%H:%M").time()
        if Sunday is None and Monday is None and Tuesday is None and Wednesday is None and Thursday is None and Friday is None and Saturday is None:
            messages.add_message(request,messages.ERROR,"At least select one day")
            return HttpResponseRedirect(reverse("pharmacy_update", kwargs={'id':request.user.id}))
        if opening_time >= close_time and break_start_time >= close_time and break_end_time >= close_time and opening_time >= break_start_time  and opening_time >= break_end_time and break_start_time >= break_end_time:
            messages.add_message(request,messages.ERROR,"Time does not match kindly set Proper time ")
            print(messages.error)
            return HttpResponseRedirect(reverse("pharmacy_update", kwargs={'id':request.user.id})) 

        print("we are indside a add hspitals")
        try:
            
            opd = OPDTime.objects.get(user=request.user)
            opd.delete()
            opdtime= OPDTime(user=request.user,opening_time=opening_time,close_time=close_time,break_start_time=break_start_time,break_end_time=break_end_time,sunday=Sunday,monday=Monday,tuesday=Tuesday,wednesday=Wednesday,thursday=Thursday,friday=Friday,saturday=Saturday,is_active=True)
            opdtime.save()
            pharmacy = Pharmacy.objects.get(admin=request.user.id)
            pharmacy.pharmacy_name=pharmacy_name
            pharmacy.about=about
            pharmacy.registration_number=registration_number
            pharmacy.address=address
            pharmacy.city=city
            pharmacy.pin_code=pin_code
            pharmacy.state=state
            pharmacy.country=country
            pharmacy.landline=landline

            if profile_pic:
                fs=FileSystemStorage()
                filename1=fs.save(profile_pic.name,profile_pic)
                profile_pic_url=fs.url(filename1)
                pharmacy.profile_pic=profile_pic_url

            print(registration_proof)
            if registration_proof:
                fs=FileSystemStorage()
                filename=fs.save(registration_proof.name,registration_proof)
                registration_proof_url=fs.url(filename)
                pharmacy.registration_proof=registration_proof_url
            pharmacy.establishment_year=establishment_year
            pharmacy.alternate_mobile=alternate_mobile
            pharmacy.website=website
            pharmacy.linkedin=linkedin
            pharmacy.facebook=facebook
            pharmacy.instagram=instagram
            pharmacy.twitter=twitter
            pharmacy.is_appiled=True
            pharmacy.is_verified=False
            pharmacy.save()
            #edit customUSer
            pharmacy.admin.first_name=first_name
            pharmacy.admin.last_name=last_name
            pharmacy.admin.name_title=name_title       
            pharmacy.admin.save()           
                    
            
            print("All data saved")

            messages.add_message(request,messages.SUCCESS,"Succesfully Updated")
            
        except Exception as e:
            messages.add_message(request,messages.ERROR,e)
            
        return HttpResponseRedirect(reverse("pharmacy_update"))
    
class ViewPharmacyAppointmentViews(SuccessMessageMixin,View):
    def get(self, request, *args, **kwargs):
        try:
            picturesformedicine = PicturesForMedicine.objects.filter(pharmacy=request.user.pharmacy,is_active=True,is_cancelled = False)
        except Exception as e:
            messages.add_message(request,messages.ERROR,e)
            return HttpResponseRedirect(reverse("view_pharmacy_appointment"))        
        param={'picturesformedicine':picturesformedicine}
        return render(request,"pharmacy/manage_appointment.html",param)        

    def post(self, request, *args, **kwargs):
        id = request.POST.get('a_id')        
        status = request.POST.get('status')
        print(id,status)
        is_accepted = False
        is_taken = False
        is_rejected =False
        is_applied = False        
        try:
            booking = PicturesForMedicine.objects.get(id=id)
            showtime = datetime.datetime.now(tz=IST)
            print(status)
        
            if status == 'accepted':
                is_accepted = True
                booking.accepted_date= showtime
            elif status == 'taken':
                is_taken= True
                booking.taken_date= showtime
                # treatmentreliefpetient = TreatmentReliefPetient(patient=booking.patient.patients,booking=booking,status="CHECKUPED",amount_paid=booking.service.service_charge,is_active=True)
                # treatmentreliefpetient.save()
            elif status == 'rejected':
                is_rejected = True
                booking.rejected_date= showtime
            else:
                is_applied =True
            booking.is_accepted=is_accepted
            booking.is_rejected=is_rejected
            booking.is_taken=is_taken
            booking.status=status        
            booking.is_applied=is_applied
            booking.save()
            return HttpResponse("ok")
        except Exception as e:
            return HttpResponse(e)

    
def UpdloadInvoicePharmacy(request,id):
    store_invoice = request.FILES.get('store_invoice') 
    amount = request.POST.get('amount')   
    desc = request.POST.get('desc')
    try:
        booking = get_object_or_404(PicturesForMedicine,id=id)
        if store_invoice:
            print()
            fs=FileSystemStorage()
            filename1=fs.save(store_invoice.name,store_invoice)
            report_url=fs.url(filename1)
            booking.store_invoice=report_url
            booking.amount=amount
            booking.desc = desc
            booking.save()
        messages.add_message(request,messages.SUCCESS,"invoice Successfully Uploaded")
        return HttpResponseRedirect(reverse("view_pharmacy_appointment"))
    except Exception as e:
        messages.add_message(request,messages.SUCCESS,e)
        return HttpResponseRedirect(reverse("view_pharmacy_appointment"))

    
    pass

class ViewImageViews(ListView):
    pass

def deleteServicesViews(request,id):
    booking = get_object_or_404(PicturesForMedicine,id=id)
    booking.is_active =False
    booking.save()
    messages.add_message(request,messages.SUCCESS,"Appointment Successfully Deleted")
    return HttpResponseRedirect(reverse("view_pharmacy_appointment"))