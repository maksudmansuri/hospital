from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import CreateView
from .models import CustomUser
from .EmailBackEnd import EmailBackEnd


class AdminSingup(SuccessMessageMixin,CreateView):
    template_name="accounts/adminSingup.html"
    model=CustomUser
    fields=["first_name","last_name","email","phone","username","password"]
    success_message = "Hospital User Created"  
    def form_valid(self,form):
        #Saving Custom User Object for Adminhod User
        print('i m here at admin singup')
        user=form.save(commit=False)
        user.user_type=1
        user.is_active=True
        user.set_password(form.cleaned_data["password"])
        print('just one step ahead save?')   
        user.counter += 1  # Update Counter At every Call
        user.save() # Save the data
        
        return HttpResponseRedirect(reverse("dologin"))
        # else:
        #     messages.add_message(self.request,messages.ERROR,"OTP sending Failed") 
        #     return HttpResponseRedirect(reverse("hospitalsingup"))
        # Using Multi-Threading send the OTP Using Messaging Services like Twilio or Fast2sms
        
        # return HttpResponseRedirect(reverse("OTP_Gen",kwargs={"user":user.phone}))  # send to next page with OTP
