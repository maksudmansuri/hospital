from accounts.models import CustomUser
from django.urls import reverse
from django.shortcuts import render
from django.http.response import HttpResponseRedirect


def profilePicUpload(request):
    if request.method == "POST":
        user = CustomUser.objects.get(id=request.user.id)
        profile_pic = request.POST.get("profile_pic_file")
        user.profile_pic =profile_pic
        user.save()
        if user.user_type == "1":
            return HttpResponseRedirect(reverse("radmin_home"))    
        if user.user_type == "2":
            return HttpResponseRedirect(reverse("hospital_dashboard"))    
        if user.user_type == "3":
            return HttpResponseRedirect(reverse("hospital_dashboard"))    
        if user.user_type == "4":
            return HttpResponseRedirect(reverse("hospital_dashboard"))    
        if user.user_type == "5":
            return HttpResponseRedirect(reverse("hospital_dashboard"))    
        if user.user_type == "6":
            return HttpResponseRedirect(reverse("hospital_dashboard"))              
    return render(request,"accounts/profile_picUpload.html")