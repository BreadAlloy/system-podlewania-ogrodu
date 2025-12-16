from django.contrib import admin
from django.urls import path, include
from apps.SPO.views import ZaworyView, ZaworCreateView, ZaworONOFFView, WodomierzView, LogiView, PlanProgramowView, ProgramRemoveView, ProgramCreateView, ProgramEditView

urlpatterns = [
    path("", ZaworyView.as_view(), name="landing"),
    path("zawory/", ZaworyView.as_view(), name="zawory"),
    path("zawory/create", ZaworCreateView.as_view(), name="zawor_create"),
    path("zawory/<int:zawor_id>/", ZaworONOFFView, name="switch"),
    path("wodomierz/", WodomierzView.as_view(), name="wodomierz"),
    path("plan/",PlanProgramowView.as_view(), name="plan_programow"),
    path('logi/', LogiView.as_view(), name='logi'),
    path('plan/remove/<str:program_name>',ProgramRemoveView, name="program_remove"),
    path('plan/create/',ProgramCreateView, name="program_create"),
    path('plan/edit/<str:program_name>',ProgramEditView, name="program_edit"),
]
