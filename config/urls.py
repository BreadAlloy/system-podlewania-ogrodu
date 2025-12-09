from django.contrib import admin
from django.urls import path, include
from apps.SPO.views import ZaworyView, ZaworCreateView, ZaworONOFFView, WodomierzView, LogiView

urlpatterns = [
    path("", ZaworyView.as_view(), name="landing"),
    path("zawory/", ZaworyView.as_view(), name="zawory"),
    path("zawory/create", ZaworCreateView.as_view(), name="zawor_create"),
    path("zawory/<int:zawor_id>/", ZaworONOFFView, name="switch"),
    path("wodomierz/", WodomierzView.as_view(), name="wodomierz"),
    path('logi/', LogiView.as_view(), name='logi')
]