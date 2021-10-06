
from patient.models import LabTest, Orders, Slot, phoneOPTforoders
from lab.models import Medias
from hospital.models import ServiceAndCharges
from django.core.files.storage import FileSystemStorage
from accounts.models import CustomUser, Labs, OPDTime
from django.contrib.messages.views import SuccessMessageMixin
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView
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
                return render(request,"lab/index.html")
            
            
            # messages.add_message(request,messages.ERROR,"Some detail still Missing !")
            # param={'hospital':hospital,'insurances':insurances,'contacts':contacts}
            # return render(request,"hospital/hospital_update.html",param)
       
    # def get(self,request):
    #     print("hello in m  in lab")
    #     return render(request,"lab/index.html")
    
class LabUpdateViews(SuccessMessageMixin,UpdateView):
    def get(self, request, *args, **kwargs):
        # hospital = None
        # # contacts = None
        # # insurances = None
        try:
            lab = Labs.objects.get(admin=request.user)
            opdtime=OPDTime.objects.get(user=request.user)
        except Exception as e:
            return HttpResponse(e)
        param={'lab':lab,'opdtime':opdtime}
        return render(request,"lab/lab_update.html",param) 
    
    def post(self, request, *args, **kwargs):
        lab_name = request.POST.get("lab_name")
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

        #Schedule for Labs OPD and Appointment
        
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
            lab = Labs.objects.get(admin=request.user.id)
            lab.lab_name=lab_name
            lab.about=about
            lab.registration_number=registration_number
            lab.address=address
            lab.city=city
            lab.pin_code=pin_code
            lab.state=state
            lab.country=country
            lab.landline=landline

            if profile_pic:
                fs=FileSystemStorage()
                filename1=fs.save(profile_pic.name,profile_pic)
                profile_pic_url=fs.url(filename1)
                lab.profile_pic=profile_pic_url

            print(registration_proof)
            if registration_proof:
                fs=FileSystemStorage()
                filename=fs.save(registration_proof.name,registration_proof)
                registration_proof_url=fs.url(filename)
                lab.registration_proof=registration_proof_url
            lab.establishment_year=establishment_year
            lab.alternate_mobile=alternate_mobile
            lab.website=website
            lab.linkedin=linkedin
            lab.facebook=facebook
            lab.instagram=instagram
            lab.twitter=twitter
            lab.is_appiled=True
            lab.is_verified=False
            lab.save()
            #edit customUSer
            lab.admin.first_name=first_name
            lab.admin.last_name=last_name
            lab.admin.name_title=name_title       
            lab.admin.save()           
                    
            
            print("All data saved")

            messages.add_message(request,messages.SUCCESS,"Succesfully Updated")
            
        except Exception as e:
            messages.add_message(request,messages.ERROR,e)
            
        return HttpResponseRedirect(reverse("lab_update"))

class ServicesViews(SuccessMessageMixin,CreateView):
    def get(self, request, *args, **kwargs):
        try:
            lab = Labs.objects.get(admin=request.user)
            serviceandcharges = ServiceAndCharges.objects.filter(user=request.user,is_active=True)
        except Exception as e:
            return HttpResponse(e)
        param={'lab':lab,'serviceandcharges':serviceandcharges}
        return render(request,"lab/service_and_prices.html",param) 

    def post(self, request, *args, **kwargs):
        try:
            if request.method == "POST":
                service_name=request.POST.get('service_name')
                service_charge=request.POST.get('service_charge')
              
                serviceandcharges = ServiceAndCharges(user=request.user,service_name=service_name,service_charge=service_charge,is_active=True)
                serviceandcharges.save()
                messages.add_message(request,messages.SUCCESS,"Succesfully Added")
        except Exception as e:
            messages.add_message(request,messages.ERROR,e)
            
        return HttpResponseRedirect(reverse("add_lab_services"))

def UpdateServicesViews(request):
    if request.method == "POST":
        service_name = request.POST.get("service_name")
        id = request.POST.get("id")
        service_charge = request.POST.get("service_charge")
        serviceandcharges = get_object_or_404(ServiceAndCharges,id=id)
        serviceandcharges.service_name=service_name
        serviceandcharges.service_charge=service_charge
        serviceandcharges.save()
        messages.add_message(request,messages.SUCCESS,"Successfully Update")
    return HttpResponseRedirect(reverse("add_lab_services"))

def deleteServicesViews(request,id):
    service = service =get_object_or_404(ServiceAndCharges,id=id)
    service.is_active = False
    service.save()
    messages.add_message(request,messages.SUCCESS,"Successfully Delete")
    return HttpResponseRedirect(reverse("add_lab_services"))

class ManageMainGalleryView(SuccessMessageMixin,CreateView):
    def get(self, request, *args, **kwargs):
        try:
            user= get_object_or_404(CustomUser,id=request.user.id)
            medias = Medias.objects.filter(user=user)
        except Exception as e:
            messages.add_message(request,messages.ERROR,"user not available")
            return HttpResponseRedirect(reverse("manage_main_gallery"))        
        param={'medias':medias}
        return render(request,"lab/manage_main_gallery.html",param)        

    def post(self, request, *args, **kwargs):
        media_type_list = request.POST.get('media_type')        
        media_content_list = request.FILES.getlist('media_content[]')        
        media_desc_list = request.POST.get('media_desc') 
        user= get_object_or_404(CustomUser,id=request.user.id)
        
        i=0
        for media_content in media_content_list:
            fs=FileSystemStorage()
            filename=fs.save(media_content.name,media_content)
            media_url=fs.url(filename)
            hospital_media = Medias(user=user,media_type=media_type_list,media_desc=media_desc_list,media_content=media_url)
            hospital_media.is_active=True
            hospital_media.save() 
            i=i+1  
            print("Meida saved")      
        return HttpResponseRedirect(reverse("manage_main_gallery"))

def deleteMainGallery(request):
    if request.method == "POST":
        checked_list = request.POST.getlist("id[]")
        print(checked_list)
        for deletecheck in checked_list:
            hospital_media = Medias.objects.get(id=deletecheck)
            hospital_media.delete()
        messages.add_message(request,messages.SUCCESS,"Successfully gellery Deleted")
        return HttpResponseRedirect(reverse("manage_main_gallery"))

class ViewAppointmentViews(SuccessMessageMixin,View):
    def get(self, request, *args, **kwargs):
        try:
            bookings = Slot.objects.filter(lab=request.user.labs,is_active=True,is_cancelled = False)
            booking_labtest_list =[] 
            for booking in bookings:
                labtest = LabTest.objects.filter(slot=booking)
                booking_labtest_list.append({'booking':booking,'labtest':labtest})
        except Exception as e:
            messages.add_message(request,messages.ERROR,e)
            return HttpResponseRedirect(reverse("view_lab_appointment"))        
        param={'booking_labtest_list':booking_labtest_list}
        return render(request,"lab/manage_appointment.html",param)        

    def post(self, request, *args, **kwargs):
        id = request.POST.get('a_id')        
        status = request.POST.get('status')
        is_accepted = False
        is_taken = False
        is_rejected =False
        is_applied = False        
        try:
            booking = get_object_or_404(Slot, id=id)
            showtime = datetime.now(tz=IST)
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
            print(booking)
            return HttpResponse("ok")
        except Exception as e:
            return HttpResponse(e)

def verifylabtestbooking(request):
    if request.POST:
        try:
            id = request.POST.get("slot_id")
            booking = Slot.objects.get(id=id)
            order = get_object_or_404(Orders,booking_for=2,bookingandlabtest=id)
            phoneotp = get_object_or_404(phoneOPTforoders, order_id = order)
            user = phoneotp.user #mobile is a user     
        
            postotp=request.POST.get("otp")
            
            showtime = datetime.now(tz=IST)
            key = phoneotp.otp  # Generating Key
            print(key)
            print(postotp)
            if postotp == str(key):  # Verifying the OTP
                order.is_booking_Verified = True
                order.save()
                phoneotp.validated = True          
                phoneotp.save()
                is_taken= True
                booking.is_taken=is_taken
                booking.status="taken"        
                booking.taken_date= showtime
                booking.save()
                messages.add_message(request,messages.SUCCESS,"booking have been Verified Successfuly")
            else:
                messages.add_message(request,messages.ERROR,"OTP does not matched")
            return HttpResponseRedirect(reverse("view_lab_appointment"))
            #emila message for email verification
            # current_site=get_current_site(request) #fetch domain    
            # email_subject='Confirmation email for you booking order',
            # message=render_to_string('accounts/activate.html',
            # {
            #     'user':user,
            #     'domain':current_site.domain,
            #     'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token':generate_token.make_token(user)
            # } #convert Link into string/message
            # )
            # print(message)
            # email_message=EmailMessage(
            #     email_subject,
            #     message,
            #     settings.EMAIL_HOST_USER,
            #     [user.email]
            # )#compose email
            # print(email_message)
            # email_message.send() #send Email
            # messages.add_message(request,messages.SUCCESS,"Sucessfully Singup Please Verify Your Account Email")  
           
        except Exception as e:
            messages.add_message(request,messages.ERROR,e)
            return HttpResponse(e)  # False Call    
        

def dateleLabAppointment(request, id):
    booking = get_object_or_404(Slot,id=id)
    labtests = LabTest.objects.filter(slot=booking)
    for labtest in labtests:
        labtest.is_active =False
        labtest.save()
    booking.is_active = False
    booking.save()
    messages.add_message(request,messages.SUCCESS,"Appointment Successfully Deleted")
    return HttpResponseRedirect(reverse("view_lab_appointment"))

def UploadReportViews(request,id):
    report = request.FILES.get('report')        
    desc = request.POST.get('desc')
    try:
        booking = get_object_or_404(Slot,id=id)
        if report:
            print()
            fs=FileSystemStorage()
            filename1=fs.save(report.name,report)
            report_url=fs.url(filename1)
            booking.report=report_url
            booking.desc = desc
            booking.save()
        messages.add_message(request,messages.SUCCESS,"Report Successfully Uploaded")
        return HttpResponseRedirect(reverse("view_lab_appointment"))
    except Exception as e:
        messages.add_message(request,messages.SUCCESS,e)
        return HttpResponseRedirect(reverse("view_lab_appointment"))

    
    
