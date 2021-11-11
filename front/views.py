from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse
from django.views.generic import View

from django.contrib import messages

from accounts.models import Hospitals
# Create your views here.

class FrontView(View):
    def get(self, request, *args, **kwargs):
        # try:
        #     hospital=Hospitals.objects.get(admin=request.user)
        #     # departments = Departments.objects.filter(hospital=hospital)
        # except Exception as e:
        #     messages.add_message(request,messages.ERROR,"something went wrong")
        #     # return HttpResponseRedirect(reverse("manage_staff"))        
        # param={'hospital':hospital}
        return render(request,"front/index.html")
