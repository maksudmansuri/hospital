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
    path('update_department',views.updateDepartment,name="update_department"),

    #deaprtment manage add update delete 
    path('manage_room',views.manageRoomclassView.as_view(),name="manage_room"),
    path('update_room',views.updateRoom,name="update_room"),


    #active deactive staff
    path('active_staff/<id>',views.activeStaff,name="active_staff"),
    path('deactive_staff/<id>',views.deactiveStaff,name="deactive_staff"),
    path('delete_staff/<id>',views.deleteHospitalStaff,name="delete_staff"),
    #active deactive department
    path('active_department/<id>',views.activeDepartment,name="active_department"),
    path('deactive_department/<id>',views.deactiveDepartment,name="deactive_department"),
    path('delete_department/<id>',views.deleteHospitalDepartment,name="delete_department"),
    #active deactive rooms
    path('active_room/<id>',views.activeRoom,name="active_room"),
    path('deactive_room/<id>',views.deactiveRoom,name="deactive_room"),
    path('delete_room/<id>',views.deleteHospitalRoom,name="delete_room"),
    # path('add_staff',views.addStaffView.as_view(),name="add_staff"),
    #delete price add price
    path('add_price',views.PriceCreate,name="add_price"),
    path('delete_price/<id>',views.deletePrice,name="delete_price"),
]  