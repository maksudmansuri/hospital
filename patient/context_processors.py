from .basket import Basket


def basket(request):
    return {'basket':Basket(request)}

def notificationprocessors(request):
    return {'room_name': "broadcast"}