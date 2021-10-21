from channels.generic.websocket import WebsocketConsumer
import json
from .models import *
from asgiref.sync import async_to_sync , sync_to_async

class BookingProgress(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['booking_id']
        self.room_group_name = 'booking_%s' % self.room_name
        print("connect")
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name 
        )
        self.accept()
        booking = Booking.give_booking_details(self.room_name)
        self.send(text_data=json.dumps({
            "payload" : booking
        }))

    def disconnect(self):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type' : 'booking_status',
                'payload' : text_data
            }
        )
       
    def booking_status(self ,event):
        print(event)
        booking = json.loads(event['value'])
        self.send(text_data=json.dumps({
            'payload' : booking
        }))

class SlotProgress(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['booking_id']
        self.room_group_name = 'booking_%s' % self.room_name
        print("connect")
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name 
        )
        self.accept()
        booking = Slot.give_slot_details(self.room_name)
        self.send(text_data=json.dumps({
            "payload" : booking
        }))

    def disconnect(self):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type' : 'slot_status',
                'payload' : text_data
            }
        )

    def slot_status(self ,event): 
        print(event)
        booking = json.loads(event['value'])
        self.send(text_data=json.dumps({
            'payload' : booking
        }))


class PictureProgress(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['booking_id']
        self.room_group_name = 'booking_%s' % self.room_name
        print("connect")
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name 
        )
        self.accept()
        booking = PicturesForMedicine.give_picture_details(self.room_name)
        self.send(text_data=json.dumps({
            "payload" : booking
        }))

    def disconnect(self):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type' : 'pictureformedicine_status',
                'payload' : text_data
            }
        )

    def pictureformedicine_status(self ,event): 
        print(event)
        booking = json.loads(event['value'])
        self.send(text_data=json.dumps({
            'payload' : booking
        }))
