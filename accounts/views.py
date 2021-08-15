from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
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
# Create your views here.


# This class returns the string needed to generate the key
class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now())) + "Some Random Secret Key"
 
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
                    else:
                        return HttpResponseRedirect(reverse('admin:index'))
                if user.user_type=="2":
                    if 'next' in request.POST:
                        return redirect(request.POST.get('next'))
                    else:
                        return HttpResponseRedirect(reverse('admin_home'))
                elif user.user_type=="3":
                    if 'next' in request.POST:
                        return redirect(request.POST.get('next'))
                    else:
                        return HttpResponseRedirect(reverse('admin_home'))
                elif user.user_type=="4":
                    if 'next' in request.POST:
                        return redirect(request.POST.get('next'))
                    else:
                        return HttpResponseRedirect(reverse('home'))
                else:
                # For Djnago default Admin Login return HttpResponseRedirect(reverse('admin:index'))
                    return HttpResponseRedirect(reverse('admin_home'))
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
        print(message)
        print(urlsafe_base64_encode(force_bytes(user.pk)),)
        print(generate_token.make_token(user))
        print(current_site.domain)
        email_message=EmailMessage(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email]
        )
        print(email_message)
        email_message.send()
        msg=messages.success(self.request,"Sucessfully Singup Please Verify Your Account First")
        return HttpResponseRedirect(reverse("dologin"))

class DoctorSingup(SuccessMessageMixin,CreateView):
    template_name="accounts/doctorsingup.html"
    model=CustomUser
    fields=["first_name","last_name","email","phone","username","password"]
    success_message = "Hospital User Created"  
    def form_valid(self,form):
        #Saving Custom User Object for Merchant User
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
        print('i m here at dosignup')
        user=form.save(commit=False)
        user.is_active=True
        user.user_type=4
        user.set_password(form.cleaned_data["password"])
        print('just one step ahead save?')
        user.save()
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
        user.is_active=True
        user.save()
        messages.add_message(request,messages.SUCCESS,'account  is Activated Successfully')
        return redirect('/accounts/dologin')
    return render(request,'accounts/activate_failed.html',status=401)
