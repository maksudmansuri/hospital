from django.urls import path
from .import views

urlpatterns = [
    path('auth_404',views.auth404View,name="auth_404"), 
    path('auth_password_reset',views.auth_password_resetView,name="auth_password_reset"), 
    path('auth_signin',views.auth_signinView,name="auth_signin"), 
    path('auth_signup',views.auth_signupView,name="auth_signup"), 
    path('auth_two_step',views.auth_two_stepView,name="auth_two_step"), 
    path('index',views.indexView,name="index"), 
    
]