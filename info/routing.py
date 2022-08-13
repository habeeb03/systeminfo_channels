from django.urls import path
from .consumers import UpdateSystemInfo

ws_pattern = [
    path('ws/sysinfo/', UpdateSystemInfo.as_asgi())
]