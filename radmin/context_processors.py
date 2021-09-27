

from patient.models import Booking, Slot
from accounts.models import Hospitals, Labs, Pharmacy


def Badgeson(request):
    hospital_pending = Hospitals.objects.filter(admin__is_active=True,is_appiled=True,is_deactive=False).count()
    lab_pending = Labs.objects.filter(admin__is_active=True,is_appiled=True,is_deactive=False).count()
    pharmacy_pending =Pharmacy.objects.filter(admin__is_active=True,is_appiled=True,is_deactive=False).count()
    badgetotal = hospital_pending+lab_pending+pharmacy_pending
    return {'chospital':hospital_pending,'clab':lab_pending,'cpharmacy':pharmacy_pending,'badgetotal':badgetotal}

def BadgeNewAppointment(request):
    badgehosappointment=0
    badgenewappointment=0
    if request.user.is_authenticated:
        if request.user.user_type == "2":
            badgehosappointment = Booking.objects.filter(hospitalstaffdoctor__hospital =request.user.hospitals ,is_active=True,is_cancelled=False,status="",is_applied=True).count()
        elif request.user.user_type == "4":    
            badgenewappointment = Slot.objects.filter(lab__admin =request.user,is_active=True,is_cancelled=False,status="",is_applied=True).count()
            print(badgenewappointment)

    return{'badgelabappointment':badgenewappointment,'badgehosappointment':badgehosappointment}