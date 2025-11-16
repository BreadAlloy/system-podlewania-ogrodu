from django import forms
from django.forms.models import inlineformset_factory
from .models import Zawor

class ZaworForm(forms.ModelForm):
    class Meta:
        model = Zawor
        fields = ['real_id', 'status']

class ONOFF(forms.ModelForm):
    class Meta:
        model = Zawor
        fields = ['real_id', 'status']