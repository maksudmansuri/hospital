"""
ASGI config for relief project.
It exposes the ASGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from channels import consumer
from patient.consumers import BookingProgress, PictureProgress, SlotProgress
from django.conf.urls import url

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from django.urls import path
from chat.consumers import *
from channels.auth import AuthMiddlewareStack
from whitenoise.django import DjangoWhiteNoise



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'relief.settings')

application = get_asgi_application()
application = DjangoWhiteNoise(application)

ws_patterns = [
    path('ws/notification/<user>' ,NotificationConsumer.as_asgi() ),
    path('ws/patient/<booking_id>',BookingProgress.as_asgi()),
    path('ws/patientlab/<booking_id>',SlotProgress.as_asgi()),
    path('ws/patientpicture/<booking_id>',PictureProgress.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket' : AuthMiddlewareStack(URLRouter(
        ws_patterns
        ))
})

