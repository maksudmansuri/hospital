from typing import Counter
from django.contrib.messages import views
from django.http import request, response
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls.base import reverse_lazy, translate_url
from django.views.generic.base import RedirectView, TemplateResponseMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from .models import CustomUser
from .EmailBackEnd import EmailBackEnd
from django.contrib.auth import login,logout,authenticate
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.core.mail import EmailMessage, message
from django.conf import settings
from .utils import generate_token
import base64
import pyotp
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
import random
import http.client
import ast
conn = http.client.HTTPConnection("2factor.in")
# Create your views here.


# This class returns the string needed to generate the key
class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now())) + "Some Random Secret Key"

def verifyPhone(request,phone):
    try:
        user = CustomUser.objects.get(phone=phone)
        print("inside virify phone")
    except ObjectDoesNotExist:
        messages.add_message(request,messages.ERROR,"Mobile number does not Exits")
        return render(request,"accounts/OTPVerification.html")  # False Call
    return render(request,"accounts/OTPVerification.html",{'user':user})  #  Call

def verifyOTP(request,phone):
    try:
        user = CustomUser.objects.get(phone=phone) #mobile is a user
    except ObjectDoesNotExist:
        messages.add_message(request,messages.ERROR,"Mobile number does not Exits")
        return HttpResponseRedirect(reverse("hospitalsingup"))  # False Call
    if request.POST:
        first=request.POST.get("first")
        second=request.POST.get("second")
        third=request.POST.get("third")
        forth=request.POST.get("forth")
        fifth=request.POST.get("fifth")
        sixth=request.POST.get("sixth")

        postotp = first+second+third+forth+fifth+sixth  #added in one string

        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())  # Generating Key
        OTP = pyotp.HOTP(key)  # HOTP Model
        if OTP.verify(postotp, user.counter):  # Verifying the OTP
            user.is_Mobile_Verified = True
            user.is_active=True
            user.save()
            messages.add_message(request,messages.SUCCESS,"Mobile Verified Successfuly")
        #emila message for email verification
        current_site=get_current_site(request) #fetch domain    
        email_subject='Active your Account',
        message=render_to_string('accounts/activate.html',
        {
            'user':user,
            'domain':current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user)
        } #convert Link into string/message
        )
        print(message)
        email_message=EmailMessage(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email]
        )#compose email
        print(email_message)
        email_message.send() #send Email
        messages.add_message(request,messages.SUCCESS,"Sucessfully Singup Please Verify Your Account Email")        
        return HttpResponseRedirect(reverse("dologin"))
        # return HttpResponseRedirect(reverse("dologin"))


def dologin(request):
    print(request.user)
    if request.method == "POST":
    #check user is authenticate or not
        user=EmailBackEnd.authenticate(request,username=request.POST.get("username"),password=request.POST.get("password"))
        if user is not None:
            if user.is_active == True:
                login(request,user)
                # request.session['logged in']=True
                if user.user_type=="1":
                    if 'next' in request.POST:
                        return redirect(request.POST.get('next'))
                    # elif user.profile_pic:
                    #     return HttpResponseRedirect(reverse('profile_picUpload'))
                    else:
                        return HttpResponseRedirect(reverse('radmin_home'))
                        # return HttpResponseRedirect(reverse('admin:index'))
                if user.user_type=="2":
                    if 'next' in request.POST:
                        return redirect(request.POST.get('next'))
                    # elif user.profile_pic:
                    #     return HttpResponseRedirect(reverse('profile_picUpload'))
                    else: 
                        return HttpResponseRedirect(reverse('hospital_dashboard'))
                elif user.user_type=="3":
                    if 'next' in request.POST:
                        return redirect(request.POST.get('next'))
                    # elif user.profile_pic:
                    #     return HttpResponseRedirect(reverse('profile_picUpload'))
                    else:
                        return HttpResponseRedirect(reverse('admin_home'))
                elif user.user_type=="4":
                    if 'next' in request.POST:
                        return redirect(request.POST.get('next'))
                    # elif user.profile_pic:
                    #     return HttpResponseRedirect(reverse('profile_picUpload'))
                    else:
                        return HttpResponseRedirect(reverse('patient_home'))
                else:
                # For Djnago default Admin Login 
                    return HttpResponseRedirect(reverse('admin'))
                    
                    # return RedirectView.as_view(url=reverse_lazy('admin:index'))
                    # return HttpResponseRedirect(reverse('admin_home'))
            else:
                # message.add_message(request,messages.ERROR,"Please Verify Your Account First")
                return redirect('/accounts/dologin')
        else: 
            # print(user.is_active)
            # messages.add_message(request,messages.ERROR,"User Not Found you haved to Register First")
            return redirect("dologin")
    return render(request,'accounts/dologin.html')
       
class HospitalSingup(SuccessMessageMixin,CreateView):
    template_name="accounts/hospitalsingup.html"
    model=CustomUser
    fields=["first_name","last_name","email","phone","username","password"]
    success_message = "Hospital User Created"  
    def form_valid(self,form):
        #Saving Custom User Object for Merchant User
        print('i m here at Hospital singup')
        user=form.save(commit=False)
        user.user_type=2
        user.set_password(form.cleaned_data["password"])
        print('just one step ahead save?')   
        user.counter += 1  # Update Counter At every Call
        user.save() # Save the data
        mobile= user.phone
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(mobile).encode())  # Key is generated
        OTP = pyotp.HOTP(key)  # HOTP Model for OTP is created
        print(OTP.at(user.counter))
        otp=OTP.at(user.counter)
        conn.request("GET", "https://2factor.in/API/R1/?module=SMS_OTP&apikey=f08f2dc9-aa1a-11eb-80ea-0200cd936042&to="+str(mobile)+"&otpvalue="+str(otp)+"&templatename=WomenMark1")
        res = conn.getresponse()
        data = res.read()
        data=data.decode("utf-8")
        data=ast.literal_eval(data)
        print(data)
        if data["Status"] == 'Success':
            user.otp_session_id = data["Details"]
            user.save()
            print('In validate phone :'+user.otp_session_id)
        messages.add_message(self.request,messages.SUCCESS,"OTP sent successfully") 
        return HttpResponseRedirect(reverse("verifyPhone",kwargs={'phone':user.phone}))
        # else:
        #     messages.add_message(self.request,messages.ERROR,"OTP sending Failed") 
        #     return HttpResponseRedirect(reverse("hospitalsingup"))
        # Using Multi-Threading send the OTP Using Messaging Services like Twilio or Fast2sms
        
        # return HttpResponseRedirect(reverse("OTP_Gen",kwargs={"user":user.phone}))  # send to next page with OTP

class DoctorSingup(SuccessMessageMixin,CreateView):
    template_name="accounts/doctorsingup.html"
    model=CustomUser
    fields=["first_name","last_name","email","phone","username","password"]
    success_message = "Hospital User Created"  
    def form_valid(self,form):
        #Saving Custom User Object for Doctor User
        print('i m here at dosignup')
        user=form.save(commit=False)
        user.is_active=True
        user.user_type=3
        user.set_password(form.cleaned_data["password"])
        print('just one step ahead save?')
        user.save()
        return HttpResponseRedirect(reverse("dologin"))

class PatientSingup(SuccessMessageMixin,CreateView):
    template_name="accounts/patientsingup.html"
    model=CustomUser
    fields=["first_name","last_name","email","phone","username","password"]
    success_message = "Hospital User Created" 

    def form_valid(self,form):
        #Saving Custom User Object for Merchant User
        print('i m here at Hospital singup')
        user=form.save(commit=False)
        user.user_type=4
        user.set_password(form.cleaned_data["password"])
        print('just one step ahead save?')   
        user.counter += 1  # Update Counter At every Call
        user.save() # Save the data
        print('user saved!')  
        mobile= user.phone
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(mobile).encode())  # Key is generated
        OTP = pyotp.HOTP(key)  # HOTP Model for OTP is created
        print(OTP.at(user.counter))
        otp=OTP.at(user.counter)
        # conn.request("GET", "https://2factor.in/API/R1/?module=SMS_OTP&apikey=f08f2dc9-aa1a-11eb-80ea-0200cd936042&to="+str(mobile)+"&otpvalue="+str(otp)+"&templatename=WomenMark1")
        # res = conn.getresponse()
        # data = res.read()
        # data=data.decode("utf-8")
        # data=ast.literal_eval(data)
        # print(data)
        # if data["Status"] == 'Success':
        #     user.otp_session_id = data["Details"]
        #     user.save()
        #     print('In validate phone :'+user.otp_session_id)
        messages.add_message(self.request,messages.SUCCESS,"OTP sent successfully") 
        return HttpResponseRedirect(reverse("verifyPhone",kwargs={'phone':user.phone}))

class AuthorizedSingup(SuccessMessageMixin,CreateView):
    template_name="accounts/athorizations.html"
    model=CustomUser
    fields=["email","phone","username","password"]
    success_message = "Admin User Created" 

    def form_valid(self,form):
        #Saving Custom User Object for Merchant User
        print('i m here at Hospital singup')
        user=form.save(commit=False)
        user.user_type=1
        user.is_active=True
        user.set_password(form.cleaned_data["password"])
        print('just one step ahead save?')   
        user.save() # Save the data
        return HttpResponseRedirect(reverse("dologin"))



class LabSingup(SuccessMessageMixin,CreateView):
    template_name="accounts/labsingup.html"
    model=CustomUser
    fields=["first_name","last_name","email","phone","username","password"]
    success_message = "Hospital User Created"  
    def form_valid(self,form):
        #Saving Custom User Object for Merchant User
        print('i m here at dosignup')
        user=form.save(commit=False)
        user.is_active=True
        user.user_type=5
        user.set_password(form.cleaned_data["password"])
        print('just one step ahead save?')
        user.save()
        return HttpResponseRedirect(reverse("dologin"))

class PharmacySingup(SuccessMessageMixin,CreateView):
    template_name="accounts/pharmacysingup.html"
    model=CustomUser
    fields=["first_name","last_name","email","phone","username","password"]
    success_message = "Hospital User Created"  
    def form_valid(self,form):
        #Saving Custom User Object for Merchant User
        print('i m here at dosignup')
        user=form.save(commit=False)
        user.is_active=True
        user.user_type=6
        user.set_password(form.cleaned_data["password"])
        print('just one step ahead save?')
        user.save()
        current_site=get_current_site(self.request)
        email_subject='Active your Account',
        message=render_to_string('accounts/activate.html',
        {
            'user':user,
            'domain':current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user)
        }
        )
        print(urlsafe_base64_encode(force_bytes(user.pk)),)
        print(generate_token.make_token(user))
        print(current_site.domain)
        email_message=EmailMessage(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email]
        )
        email_message.send()
        msg=messages.success(self.request,"Sucessfully Singup Please Verify Your Account First")
        return HttpResponseRedirect(reverse("dologin"))

def adminSingup(request):
    if request.method=="POST":
        username = request.POST.get('username')
        r=CustomUser.objects.filter(username=username)
        if r.count():
            msg=messages.error(request,"Username  Already Exits")
            return HttpResponseRedirect(reverse("dosingup"))

        email = request.POST.get('email')
        e=CustomUser.objects.filter(email=email)
        if e.count():        
            msg=messages.error(request,"Email Already Exits")
            return HttpResponseRedirect(reverse("dosingup"))
            
        phone = request.POST.get('phone')
        p=CustomUser.objects.filter(phone=phone)
        if p.count():
            msg=messages.error(request,"Phone Already Exits")
            return HttpResponseRedirect(reverse("dosingup"))
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 and password2 and password1 != password2:
            msg=messages.error(request,"Password Does Match")
            return HttpResponseRedirect(reverse("dosingup"))
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        print('i m here at dosignup')
        print(email,first_name,last_name,username,phone,password1)
        user=CustomUser.objects.create_user(username=username,password=password1,email=email)
        # user.save(commit=False)
        print('first name ')
        user.last_name = last_name
        print('last name ')
        user.phone=phone
        user.user_type="2"
        print('first name lats name nad phone done')
        user.first_name = first_name
        user.save()
        print('i m done my dosignup')
        # current_site=get_current_site(request)
        # email_subject='Active your Account',
        # message=render_to_string('accounts/activate.html',
        # {
        #     'user':user,
        #     'domain':current_site.domain,
        #     'uid':urlsafe_base64_encode(force_bytes(user.pk/tt)),
        #     'token':generate_token.make_token(user)
        # }
        # )
        # print(urlsafe_base64_encode(force_bytes(user.pk)),)
        # print(generate_token.make_token(user))
        # print(current_site.domain)
        # email_message=EmailMessage(
        #     email_subject,
        #     message,
        #     settings.EMAIL_HOST_USER,
        #     [email]
        # )
        # email_message.send()
        # msg=messages.success(request,"Sucessfully Singup Please Verify Your Account First")
        print("hello bhia ahiya ayo em")           
        return HttpResponseRedirect(reverse("dologin"))
        # except:
        #     msg=messages.error(request,"Connection Error Try Again")
        #     return HttpResponseRedirect(reverse("dosingup"))
    return render(request,"accounts/dosingup.html")

def activate(request,uidb64,token):
    try:
        uid=force_text(urlsafe_base64_decode(uidb64))
        print(uid)
        user=CustomUser.objects.get(pk=uid) 
    except:
        user=None
    if user is not None and generate_token.check_token(user,token):
        if user.is_Mobile_Verified:
            user.is_active=True
        user.is_Email_Verified=True
        user.save()
        messages.add_message(request,messages.SUCCESS,'account  is Activated Successfully')
        return redirect('/accounts/dologin')
    return render(request,'accounts/activate_failed.html',status=401)

# def VerifyOTP(request,phone):
#     try:
#         Mobile = CustomUser.objects.get(phone=phone)
#     except ObjectDoesNotExist:
#         messages.add_message(request,messages.ERROR,"Mobile number does not Exits")
#         return HttpResponseRedirect(reverse("OTP_Gen"))  # False Call
#     if request.POST:
#         pass
#     keygen = generateKey()
#     key = base64.b32encode(keygen.returnValue(phone).encode())  # Generating Key
#     OTP = pyotp.HOTP(key)  # HOTP Model
#     if OTP.verify(request.data["otp"], Mobile.counter):  # Verifying the OTP
#         Mobile.is_Mobile_Verified = True
#         if Mobile.is_Email_Verified:
#             Mobile.is_active=True
#         Mobile.save()
#         messages.add_message(request,messages.ERROR,"Mobile Verified Successfuly")
#     return HttpResponseRedirect(reverse("dologin"))

def logout_view(request):
    logout(request)
    return redirect('dologin')