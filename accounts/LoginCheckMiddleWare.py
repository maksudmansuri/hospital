from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin 
from django.urls import reverse
from django.shortcuts import redirect
from django.urls import path, reverse_lazy
from django.views.generic.base import RedirectView

class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self,request,views_func,view_args,view_kwargs):
        modulename=views_func.__module__

        user=request.user
        if user.is_authenticated:
            if user.user_type=="1":
                if modulename == "ecaadmin.views" or modulename == "django.views.static":
                    pass
                elif modulename == "front.views":
                    pass
                elif modulename == "media.views":
                    pass
                elif modulename == "django.contrib.auth.views":
                    pass
                elif  modulename == "chat.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("admin_home"))
            elif user.user_type=="2":
                if modulename == "staffs.views" or modulename == "django.views.static":
                    pass
                elif modulename == "front.views":
                    pass
                elif modulename == "media":
                    pass
                elif modulename == "django.contrib.auth.views":
                    pass
                elif  modulename == "chat.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("instructor_dashboard"))
            elif user.user_type=="3":
                if modulename == "customers.views" or modulename == "django.views.static":
                    pass
                elif modulename == "front.views":
                    pass
                elif modulename == "front.orderviews":
                    pass
                elif modulename == "media":
                    pass
                elif modulename == "django.contrib.auth.views":
                    pass
                elif  modulename == "chat.views":
                    pass
                elif  modulename == "front.api.views":
                    pass 
                else:
                    return HttpResponseRedirect(reverse("dashboard"))
            elif user.user_type=="4":
                if modulename == "merchant.views" or modulename == "django.views.static":
                    pass
                if modulename == "front.views":
                    pass
                elif modulename == "media":
                    pass
                # else:
                #     return redirect("/admin")
                    # return HttpResponseRedirect(reverse("django/contrib/admin"))
            elif user.user_type=="0" or user.is_superuser==True:
                if modulename == "ecaadmin.views" or modulename == "django.views.static":
                    pass
                elif modulename == "front.views":
                    pass
                elif modulename == "media.views":
                    pass
                if modulename == "django.contrib.auth.views":
                    pass
                elif  modulename == "chat.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("admin_home"))
                # if modulename == "django.contrib.auth.views":
                #     pass
                # if modulename == "front.views":
                #     pass
                    # return HttpResponseRedirect(reverse('admin_home'))
                # else:
                # return RedirectView.as_view(url=reverse_lazy('admin:index'))
                # return reverse('admin_login')
        else:
            if request.path == reverse("dologin") or modulename == "front.views" or modulename == "accounts.views" or modulename == "django.views.static" or modulename == "django.contrib.auth.views" or modulename == "chat.views" or modulename == "accounts.api.views" or modulename == "front.api.views" or request.path == reverse("login") or modulename == "allauth.account.views" or modulename == " allauth.socialaccount.views" :
                pass
            else:
                return HttpResponseRedirect(reverse("dologin")) or modulename == "allauth.account.views" or modulename == " allauth.socialaccount.views" or request.path == reverse("saccount") or modulename == "allauth.socialaccount.providers.oauth2.views"

