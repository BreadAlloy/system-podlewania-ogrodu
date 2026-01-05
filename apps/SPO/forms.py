from django import forms
from django.forms.models import inlineformset_factory
from django.core.validators import MinValueValidator
from .models import Zawor
from konfiguracja import config
from plan_podlewania import program_podlewania, tryb_podlewania_iloscia, tryb_podlewania_czasem

class ZaworForm(forms.ModelForm):
    class Meta:
        model = Zawor
        fields = ['real_id', 'status']

class ONOFF(forms.ModelForm):
    class Meta:
        model = Zawor
        fields = ['real_id', 'status']

class ProgramForm(forms.Form):
    nazwa = forms.CharField(max_length = 50)
    godzina_start = forms.TimeField(label='Godzina rozpoczęcia',input_formats=['%H:%M'],widget=forms.TimeInput(attrs={'type':'time'}))
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

    def __init__(self, program_dict, *args, **kwargs):
        print(program_dict);
        # proponuje ten formularz zcraftować z program_dicta

        super().__init__(*args, **kwargs)
                         
        for i in program_dict["sekcje"]:
            self.fields[f'sekcja_{i["id_sekcji"]}'] = forms.FloatField(
                    label=f'Sekcja {i["id_sekcji"]} - {config.rozpiska_sekcji[i["id_sekcji"]][0]} (ml)',
                    min_value=0,
                    widget=forms.NumberInput(attrs={'step':'0.1'}),
                    required=False,
                    initial = i["ilosc"]
                )