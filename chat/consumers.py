from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

from chat.models import Notification

class NotificationConsumer(WebsocketConsumer):
     
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['user']
        print(self.room_name)
        self.room_group_name = 'notificaion_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )
        self.accept()
        # notifications = Notification.give_notification_details(self.room_name)
        # print(notifications)
        # self.send(text_data=json.dumps({
        #     "payload" : notifications
        # }))

    def receive(self,text_data):
        print(text_data)
        self.send(text_data=json.dumps({'status':'we got it'})) 

    def disconnect(self):
        self.send(text_data=json.dumps({'status':'We closed'})) 


    def receive(self, text_data):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type' : 'send_notification',
                'payload' : text_data
            }
        )

    def send_notification(self,event):
        print('send notification')
        data =json.loads(event.get('value'))
        print(data)
        count = Notification.objects.filter(to_user = self.room_name,user_has_seen=False).count()
        self.send(text_data=json.dumps({'payload':data,'count':count}))
        print('send notification')

    
    
    
