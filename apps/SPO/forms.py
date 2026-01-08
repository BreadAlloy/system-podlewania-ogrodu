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

    def __init__(self, program_dict, *args, **kwargs):
        print(program_dict);

        super().__init__(*args, **kwargs)

        self.fields['nazwa'] = forms.CharField(max_length = 50, initial=program_dict["nazwa"])
        self.fields['godzina_start'] = forms.TimeField(label='Godzina rozpoczęcia',input_formats=['%H:%M'],widget=forms.TimeInput(attrs={'type':'time'}),initial=program_dict["godzina_start"])
        tryb=False
        if program_dict["tryb"]=='CZAS (min)':
            tryb=True
        self.fields['tryb_str'] = forms.BooleanField(required=False, initial=tryb)

        self.fields['co_ile_dni_podlewac'] = forms.IntegerField(label='Co ile dni podlać',validators=[MinValueValidator(1)],initial=program_dict["co_ile_dni"])
        
        dni_podlewania=[]
        for dzien in program_dict['dni_tygodnia']:
            if program_dict['dni_tygodnia'][dzien]:
                dni_podlewania.append(dzien)
        
        self.fields['w_ktore_dni_tygodnia_podlewac'] = forms.MultipleChoiceField(
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
            label='W które dni tygodnia podlewać',
            initial=dni_podlewania
        )

        for i in program_dict["sekcje"]:
            self.fields[f'sekcja_{i["id_sekcji"]}'] = forms.FloatField(
                    label=f'Sekcja {i["id_sekcji"]} - {config.rozpiska_sekcji[i["id_sekcji"]][0]} (ml)',
                    min_value=0,
                    widget=forms.NumberInput(attrs={'step':'0.1'}),
                    required=False,
                    initial = i["ilosc"]
                )