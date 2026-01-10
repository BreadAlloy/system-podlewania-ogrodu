from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView, View
from django.urls import reverse_lazy
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from .models import Zawor, Wodomierz
from .forms import ZaworForm, ONOFF, ProgramForm
from django.views import generic
from hardware import sekcje
from konfiguracja import *
from logger import logger_globalny # do odczytu logów, niekoniecznie do zapisywania
from plan_podlewania import get_biezace_programy_podlewania, program_podlewania
from komunikator import *

def request_to_dict(request):
    tryb_str = "CZAS (min)" if request['tryb_str']=='on' else "ILOSC (litry)"
    pon = True if 'Pon' in request['w_ktore_dni_tygodnia_podlewac'] else False
    wt = True if 'Wt' in request['w_ktore_dni_tygodnia_podlewac'] else False
    sr = True if 'Sr' in request['w_ktore_dni_tygodnia_podlewac'] else False
    czw = True if 'Czw' in request['w_ktore_dni_tygodnia_podlewac'] else False
    pt = True if 'Pt' in request['w_ktore_dni_tygodnia_podlewac'] else False
    sob = True if 'Sob' in request['w_ktore_dni_tygodnia_podlewac'] else False
    nd = True if 'Nd' in request['w_ktore_dni_tygodnia_podlewac'] else False

    program_dict = {
        'nazwa': request['nazwa'],
        # rzutujemy zegarek na str, bo JSON nie ogarnia obiektów
        'godzina_start': str(request['godzina_start']), 
        'tryb': tryb_str,
        'co_ile_dni': request['co_ile_dni_podlewac'],
        'dni_tygodnia': {
            'Pon': pon,
            'Wt': wt,
            'Sr': sr,
            'Czw': czw,
            'Pt': pt,
            'Sob': sob,
            'Nd': nd,
        },
        'sekcje': []
    }

    # Dodajemy info o sekcjach (tylko te, które mają > 0 podlewania)

    sekcje = [
    float(request.get(f'sekcja_{i}', 0))
    for i in range(15)
    ]

    i=0
    for sekcja in sekcje:
        # sekcja to lista [id, ilosc]
        id_sekcji = i
        ilosc = sekcja
            
        program_dict['sekcje'].append({
            'id_sekcji': id_sekcji,
            'ilosc': ilosc
        })
        i+=1
        
    return program_dict;

discord = None;
AKTYWUJ_KOMUNIKATOR = os.environ.get("AKTYWUJ_KOMUNIKATOR");
if(AKTYWUJ_KOMUNIKATOR == "True"):
    if(discord == None):
        print("Aktywuje komunikator");
        discord = komunikator("gpio-worker", config.port_do_komunikacji);
        discord.polacz();


class ZaworyView(ListView):
    model = Zawor
    template_name = 'SPO/zawory.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["zawory"] = Zawor.objects.order_by("real_id");
        return context


class ZaworCreateView(CreateView):
    model = Zawor
    fields = ['name', 'status']
    template_name = 'SPO/zawor_form.html'
    success_url = reverse_lazy('zawory')
    
    #def form_valid(self, form):
        # np. gdy byśmy chcieli ustawiać autora na zalogowanego usera: form.instance.author = self.request.user
    #    return super().form_valid(form)

def ZaworONOFFView(request, zawor_id):
    zawor = get_object_or_404(Zawor, id=zawor_id)
    if request.method == "POST":
        if zawor.status == True:
            zawor.status = False
        else:
            zawor.status = True
        
        zawor.save()
    return redirect('zawory')

class WodomierzView(TemplateView):
    template_name = "SPO/wodomierz.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sygnaly=Wodomierz.objects.get(pk=1).ilosc
        context["wodomierz_status"] = int(sygnaly)*config.ilosc_wody_na_sygnal;
        return context
    
class LogiView(View):
    def get(self, request):
        logs_info, logs_warningi, logs_krytyczne, logs_hardware = logger_globalny.przeczytaj_logi();
        return render(request, 'SPO/logi_partial.html', {'logs_info': logs_info, 'logs_warningi': logs_warningi, 'logs_krytyczne': logs_krytyczne, 'logs_hardware': logs_hardware})

class PlanProgramowView(TemplateView):
    template_name = "SPO/plan.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["plan"] = get_biezace_programy_podlewania().values();
        return context
    
def ProgramRemoveView(request, program_name):
    discord.wyslij(kody_komunikatow.USUN_PROGRAM, program_name);
    return redirect('zawory')

def ProgramCreateView(request):
    if request.method == "POST":
        form = ProgramForm(request.POST)
        if form.is_valid():
        
            program = program_podlewania();

            print(form.cleaned_data)
            # poprosze coś w stylu
            # program = form.jako_program()

            #discord.wyslij(kody_komunikatow.DODAJ_PROGRAM, program);

            return redirect('zawory')
    else:
        program_dict = program_podlewania().to_dict();

        form = ProgramForm(program_dict)
    return render(request, "SPO/program_form.html", {"form": form})

def ProgramEditView(request, program_name):
    if request.method == "POST":
        form = ProgramForm(request_to_dict(request.POST))
        print(request_to_dict(request.POST))
        print(get_biezace_programy_podlewania()[program_name].to_dict())
        form.fields['nazwa'].widget.attrs['readonly'] = True
        form.is_bound=True
        if form.is_valid():

            program = program_podlewania();

            print("TEST")
            # poprosze coś w stylu
            # program = form.jako_program()

            #discord.wyslij(kody_komunikatow.ZMODYFIKUJ_PROGRAM, program);
        
            return redirect('zawory')
        else:
            print(form.errors)
    else:
        form = ProgramForm(get_biezace_programy_podlewania()[program_name].to_dict());
        form.fields['nazwa'].widget.attrs['readonly'] = True;
    return render(request, "SPO/program_form.html", {"form": form})

class AfkView(TemplateView):
    template_name = "SPO/afk.html";
