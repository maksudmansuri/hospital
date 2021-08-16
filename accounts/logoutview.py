from django.contrib.auth import logout
from django.shortcuts import redirect, render

def logout_view(request):
    logout(request)
    return redirect('dologin')