from chat.models import Notification

def headernotifications(request):
    notifications = Notification.objects.filter(to_user = request.user)
    notification_count = Notification.objects.filter(to_user = request.user,user_has_seen=False).count()
    return {'notifications':notifications,'notification_count':notification_count}

# def BadgeNewAppointment(request):
#     badgehosappointment=0
#     badgenewappointment=0
#     if request.user.is_authenticated:
#         if request.user.user_type == "2":
#             badgehosappointment = Booking.objects.filter(hospitalstaffdoctor__hospital =request.user.hospitals ,is_active=True,is_cancelled=False,status="",is_applied=True).count()
#         elif request.user.user_type == "4":    
#             badgenewappointment = Slot.objects.filter(lab__admin =request.user,is_active=True,is_cancelled=False,status="",is_applied=True).count()
#             print(badgenewappointment)

#     return{'badgelabappointment':badgenewappointment,'badgehosappointment':badgehosappointment}