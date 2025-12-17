from django import forms
from django.forms.models import inlineformset_factory
from django.core.validators import MinValueValidator
from .models import Zawor
from konfiguracja import config

class ZaworForm(forms.ModelForm):
    class Meta:
        model = Zawor
        fields = ['real_id', 'status']

class ONOFF(forms.ModelForm):
    class Meta:
        model = Zawor
        fields = ['real_id', 'status']

class ProgramForm(forms.Form):
    nazwa_programu = forms.CharField(max_length = 50)
    godzina_rozpoczecia = forms.TimeField(label='Godzina rozpoczęcia',input_formats=['%H:%M'],widget=forms.TimeInput(attrs={'type':'time'}))
    tryb_str = forms.BooleanField(required=False)
    w_ktore_dni_tygodnia_podlewac = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=[
            ("Pon", "Poniedziałek"),
            ("Wt", "Wtorek"),
            ("Sr", "Środa"),
            ("Czw", "Czwartek"),
            ("Pt", "Piątek"),
            ("Sob", "Sobota"),
            ("Nd", "Niedziela"),
        ],
        required=False,
        label='W które dni tygodnia podlewać'
    )
    co_ile_dni_podlac = forms.IntegerField(label='Co ile dni podlać',validators=[MinValueValidator(1)])

    def __init__(self, *args, items=None, **kwargs):
        super().__init__(*args, **kwargs)
                         
        for i in config.rozpiska_sekcji:
            self.fields[f'sekcja_{i}'] = forms.FloatField(
                    label=f'Sekcja {i} - {config.rozpiska_sekcji[i][0]} (ml)',
                    min_value=0,
                    widget=forms.NumberInput(attrs={'step':'0.1'}),
                    required=False
                )