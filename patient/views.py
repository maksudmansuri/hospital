from lab.models import Medias
import requests
from django.views.generic.base import View
from requests.models import Response
from hospital.models import HospitalMedias, HospitalStaffDoctorSchedual, HospitalStaffDoctors, ServiceAndCharges
from patient.models import Booking, Orders, LabTest, slot
from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from accounts.models import HospitalPhones, Hospitals, Labs, Patients
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, render
from django.views.generic.list import ListView
from django.contrib import messages
from django.urls.base import resolve, reverse
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
import json
from patient import PaytmChecksum
# Create your views here.
class patientdDashboardViews(SuccessMessageMixin,ListView):
    def get(self, request, *args, **kwargs):
        try: 
            patient = get_object_or_404(Patients, admin=request.user.id)

            if patient.fisrt_name and patient.last_name and patient.address and patient.city and patient.zip_Code and patient.state and patient.country and patient.dob and patient.profile_pic and patient.gender and patient.bloodgroup:
                return render(request,"patient/index.html")            
            
            messages.add_message(request,messages.ERROR,"Some detail still Missing !")
            
            return render(request,"patient/patient_update.html",{'patient':patient})
        except Exception as e:
            return HttpResponse(e)
    
class patientdUpdateViews(SuccessMessageMixin,UpdateView):
    def get(self, request, *args, **kwargs):
        try: 
            patient = get_object_or_404(Patients, admin=request.user.id)
            return render(request,"patient/patient_update.html",{'patient':patient})
        except Exception as e:
            return HttpResponse(e)
    
    def post(self,request, *agrs, **kwargs):
        profile_pic = request.FILES.get('profile_pic')
        name_title = request.POST.get('name_title')
        alternate_mobile = request.POST.get('alternate_mobile')
        address = request.POST.get('address')
        city = request.POST.get('city')
        zip_Code = request.POST.get('zip_Code')
        print(zip_Code)
        state = request.POST.get('state')
        print(state)
        country = request.POST.get('country')
        print(country)
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        bloodgroup = request.POST.get('bloodgroup')
        try:            
            user= request.user
            user.patients.name_title=name_title
            user.patients.fisrt_name=user.first_name
            user.patients.last_name=user.last_name
            if profile_pic:
                fs=FileSystemStorage()
                filename1=fs.save(profile_pic.name,profile_pic)
                profile_pic_url=fs.url(filename1)
                user.patients.profile_pic=profile_pic_url
                user.profile_pic = profile_pic_url
            user.patients.alternate_mobile=alternate_mobile
            user.patients.address=address
            user.patients.city=city
            user.patients.state=state
            user.patients.zip_Code=zip_Code
            user.patients.country=country
            user.patients.gender=gender
            user.patients.dob=dob
            user.patients.bloodgroup=bloodgroup
            user.patients.save()            
            user.save()
            messages.add_message(request,messages.SUCCESS,"User Detail updates Successfully !")
            return HttpResponseRedirect(reverse("patient_home"))
        except Exception as e:
            HttpResponse(e)

class HospitalListViews(ListView):
    def get(self, request, *args, **kwargs):
        hospitals = Hospitals.objects.filter(is_verified=True,is_deactive=False,admin__is_active=True)
        hospital_media_list = []
        for hospital in hospitals:
            medias = HospitalMedias.objects.filter(is_active=True,hospital=hospital)           
            hospital_media_list.append({'hospital':hospital,'medias':medias})
        print(hospital_media_list)
        param = {'hospital_media_list':hospital_media_list}  
        return render(request,"patient/hospital_list.html",param)
    
class HospitalDetailsViews(DetailView):
    def get(self, request, *args, **kwargs):
        hosital_id=kwargs['id']
        hospital = get_object_or_404(Hospitals,is_verified=True,is_deactive=False,id=hosital_id)
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
        return render(request,"patient/hospital_details.html",param)

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
        return render(request,"patient/bookappoinment.html",param)

class BookAnAppointmentViews(SuccessMessageMixin,View):
    def post(self,request, *args, **kwargs):
        if request.method == "POST":
            doctorid = request.POST.get('doctorid')
            hospitalstaffdoctor = get_object_or_404(HospitalStaffDoctors,id=doctorid)
            serviceid = request.POST.get('serviceid')
            service = ServiceAndCharges.objects.get(id=serviceid)
            date = request.POST.get('date')
            time = request.POST.get('time') 
            print(doctorid,hospitalstaffdoctor,serviceid,service,date,time)
            booking = Booking(patient = request.user,hospitalstaffdoctor=hospitalstaffdoctor,service=service,applied_date=date,applied_time=time,is_applied=True,is_active=True,amount=service.service_charge)
            print("booking saved")
            order = Orders(patient=request.user,service=service,amount=service.service_charge,status=1)
            order.save()
            print("order saved")
            booking.save()
            
            # import checksum generation utility
            # You can get this utility from https://developer.paytm.com/docs/checksum/
          
            # paytmParams = dict()

            # paytmParams["body"] = {
            #     "requestType"   : "Payment",
            #     "mid"           : "Vsrdcl31860853647501",
            #     "websiteName"   : "WEBSTAGING",
            #     "orderId"       : str(booking.id),
            #     "callbackUrl"   : "http://127.0.0.1:8000/patient/handlerequest",
            #     "txnAmount"     : {
            #         "value"     : str(booking.amount),
            #         "currency"  : "INR",
            #     },
            #     "userInfo"      : {
            #         "custId"    : str(request.user.phone),
            #     },
            # }

            # # Generate checksum by parameters we have in body
            # # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys 
            # checksum = PaytmChecksum.generateSignature(json.dumps(paytmParams["body"]), "JDhgGD%hhT&OtVEE")

            # paytmParams["head"] = {
            #     "signature"    : checksum
            # }
            

            # post_data = json.dumps(paytmParams)

            # # for Staging
            # url = "https://securegw.paytm.in/theia/api/v1/initiateTransaction?mid=Vsrdcl31860853647501&orderId="+str(booking.id)

            # # for Production
            # # url = "https://securegw.paytm.in/theia/api/v1/initiateTransaction?mid=YOUR_MID_HERE&orderId=ORDERID_98765"
            # response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
            # print(response)
            # print(response['body']['txnToken'])
            
           
            # paytmParams["head"] = {
            #     "tokenType"     : "TXN_TOKEN",
            #     "token"         : response['body']['txnToken']
            # }
            # post_data = json.dumps(paytmParams)

            # # for Staging
            # url = "https://securegw-stage.paytm.in/theia/api/v2/fetchPaymentOptions?mid=Vsrdcl31860853647501&orderId="+str(booking.id)
            

            # # for Production
            # # url = "https://securegw.paytm.in/theia/api/v2/fetchPaymentOptions?mid=YOUR_MID_HERE&orderId=ORDERID_98765"
            # response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
            # print(response)        

class ViewBookedAnAppointmentViews(SuccessMessageMixin,View):
    def get(self,request):
        booked = Booking.objects.filter(patient = request.user)
        print(booked)
        param = {'booked':booked}
        return render(request,"patient/appointmentlist.html",param)

def CancelBookedAnAppointmentViews(request,id):
    booked = Booking.objects.get(id=id)
    booked.is_cancelled = True
    booked.save()
    return HttpResponseRedirect(reverse('viewbookedanappointment'))
 
class BookAnAppointmentForLABViews(SuccessMessageMixin,View):
    def post(self,request, *args, **kwargs):
        if request.method == "POST":
            serviceid_list = request.POST.getlist('serviceid[]')
            print(serviceid_list)
            date = request.POST.get('date')
            time = request.POST.get('time') 
            labbooking = slot(patient = request.user,applied_date=date,applied_time=time,is_applied=True,is_active=True) 
            labbooking.save()
            total = 0
            for serviceid in serviceid_list:          
                service = ServiceAndCharges.objects.get(id=serviceid)
                labservices = LabTest(service=service,slot=labbooking,is_active=True)
                labservices.save()
                total =total + service.service_charge 
            print("booking saved")
            order = Orders(patient=request.user,service=service,amount=total,status=1)
            order.save()
            print("order saved")
            return HttpResponse("ok")
            
           


class LabListViews(ListView):
    def get(self, request, *args, **kwargs):
        labs = Labs.objects.filter(is_verified=True,is_deactive=False,admin__is_active=True)
        lab_media_list = []
        for lab in labs:
            medias = Medias.objects.filter(is_active=True,user=lab.admin)           
            lab_media_list.append({'lab':lab,'medias':medias})
        print(lab_media_list)
        param = {'lab_media_list':lab_media_list}  
        return render(request,"patient/lab_list.html",param)
    
class labDetailsViews(DetailView):
    def get(self, request, *args, **kwargs):
        lab_id=kwargs['id']
        lab = get_object_or_404(Labs,is_verified=True,is_deactive=False,id=lab_id)
        services = ServiceAndCharges.objects.filter(user=lab.admin)        
        param = {'lab':lab,'services':services}  
        return render(request,"patient/lab_details.html",param)







@csrf_exempt
def handlerequest(request):
    #paytm will send you post request here
    print("paytm came")
    # paytmParams = dict()
    # paytmChecksum = "CHECKSUM_VALUE"
    # paytmParams = request.form.to_dict()
    # paytmChecksum = paytmChecksum
    # paytmChecksum = paytmParams['CHECKSUMHASH']
    # paytmParams.pop('CHECKSUMHASH', None)

    # # Verify checksum
    # # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys 
    # isVerifySignature = PaytmChecksum.verifySignature(paytmParams, "JDhgGD%hhT&OtVEE", paytmChecksum)
    # if isVerifySignature:
    #     print("Checksum Matched")
    # else:
    #     print("Checksum Mismatched")
    pass
