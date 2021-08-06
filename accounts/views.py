from django.shortcuts import render

# Create your views here.

def auth404View(request): 
    return render(request,"accounts/auth-404.html")

def auth_password_resetView(request): 
    return render(request,"accounts/auth-password-reset.html")
def auth_signinView(request): 
    return render(request,"accounts/auth-signin.html")
def auth_signupView(request): 
    return render(request,"accounts/auth-signup.html")
def auth_two_stepView(request): 
    return render(request,"accounts/auth-two-step.html")
def indexView(request): 
    return render(request,"accounts/index.html")