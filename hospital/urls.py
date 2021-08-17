from django.urls import path
from .import views

urlpatterns = [  
    # path('',views.indexView,name="hospital_home"),
    path('',views.hospitaldDashboardViews.as_view(),name="hospital_dashboard"),
    path('hospital_update',views.hospitalUpdateViews.as_view(),name="hospital_update"),
    
    #Staff list ,add ,update ,delete
    path('manage_staff',views.manageStaffView.as_view(),name="manage_staff"),
    path('update_staff',views.updateStaff,name="update_staff"),
    
    #deaprtment manage add update delete 
    path('manage_department',views.manageDepartmentclassView.as_view(),name="manage_department"),


    #active deactive
    path('active_staff/<id>',views.activeStaff,name="active_staff"),
    path('deactive_staff/<id>',views.deactiveStaff,name="deactive_staff"),
    path('delete_staff/<id>',views.deleteHospitalStaff,name="delete_staff"),
    # path('add_staff',views.addStaffView.as_view(),name="add_staff"),
]  