from chat.models import Notification
from patient.models import Booking, PicturesForMedicine, Slot
from datetime import datetime

def headernotifications(request):
    notifications = None
    notification_count = 0
    try:
        notifications = Notification.objects.filter(to_user = request.user,user_has_seen=False)
        notification_count = Notification.objects.filter(to_user = request.user,user_has_seen=False).count()
        print(notifications,notification_count)
        return {'notifications':notifications,'notification_count':notification_count}
    except:
        return {'notifications':notifications,'notification_count':notification_count}

def patientcancel(request):
    timeleft = 0
    print(datetime.now())
    try:
        booking = Booking.objects.filter(patient = request.user).first()
        print(booking)
        print(booking.created_at)   
        slot = Slot.objects.filter(patient = request.user).first()
        print(slot)
        picturesformedicine = PicturesForMedicine.objects.filter(patient = request.user).first()
        print(picturesformedicine)
        print(":hello")
        timenow = datetime.now() - booking.created_at
        timenow1 = datetime.now() - slot.created_at
        timenow2 = datetime.now() - picturesformedicine.created_at
        print(timenow.total_seconds() / (60 * 60))
        print(timenow1)
        print(timenow2)
        if timenow.total_seconds() < 300  or timenow1.total_seconds() < 300 or timenow2.total_seconds() < 300:
            timeleft = timenow.total_seconds()
            print(timeleft)
            return {'timeleft':timeleft}
        else:
            return {'timeleft':timeleft}
        
    except:
        return {'timeleft':timeleft}
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