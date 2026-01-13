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
from czas import zegarek
import time

def form_to_program(form_data):
    print(form_data)
    program = program_podlewania()
    program.nazwa_programu=form_data['nazwa_programu']
    czas=zegarek()
    czas.godzina=form_data['godzina_rozpoczecia'].hour
    czas.minuta=form_data['godzina_rozpoczecia'].minute
    program.godzina_rozpoczecia=czas
    program.tryb_podlewania=form_data['tryb_str']
    lista_dni=[]
    for dzien in ['Pon','Wt','Sr','Czw','Pt','Sob','Nd']:
        if dzien in form_data['w_ktore_dni_tygodnia_podlewac']:
            lista_dni.append(True)
        else:
            lista_dni.append(False)
    program.w_ktore_dni_tygodnia_podlewac=lista_dni
    for i in range(0, len(program.ilosci_podlewania)):
        program.zmodyfikuj_ilosc(i,form_data['sekcja_'+str(i)])
    return program

discord = None;
AKTYWUJ_KOMUNIKATOR = os.environ.get("AKTYWUJ_KOMUNIKATOR");
if(AKTYWUJ_KOMUNIKATOR == "True" or AKTYWUJ_KOMUNIKATOR == "true" or AKTYWUJ_KOMUNIKATOR == "TRUE"):
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
        context["wodomierz_status"] = float(sygnaly)*config.ilosc_wody_na_sygnal / 10.0**6;
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
        
            program = form_to_program(form.cleaned_data)
            discord.wyslij(kody_komunikatow.DODAJ_PROGRAM, program);

            return redirect('zawory')
    else:
        form = ProgramForm()
    return render(request, "SPO/program_form.html", {"form": form})

def ProgramEditView(request, program_name):
    if request.method == "POST":
        form = ProgramForm(request.POST)
        form.fields['nazwa_programu'].widget.attrs['readonly'] = True
        if form.is_valid():

            program = form_to_program(form.cleaned_data)
            discord.wyslij(kody_komunikatow.ZMODYFIKUJ_PROGRAM, program);
        
            return redirect('zawory')
        else:
            print(form.errors)
    else:
        p_dict=get_biezace_programy_podlewania()[program_name].to_dict()

        tryb_str = True if p_dict['tryb']=="CZAS (min)" else False

        lista_dni=[]
        for dzien in p_dict['dni_tygodnia']:
            if p_dict['dni_tygodnia'][dzien]:
                lista_dni.append(dzien)

        formvaluedict={
                        'nazwa_programu':program_name,
                        'tryb_str':tryb_str,
                        'godzina_rozpoczecia':p_dict['godzina_start'],
                        'co_ile_dni_podlac':p_dict['co_ile_dni'],
                        'w_ktore_dni_tygodnia_podlewac':lista_dni,
                        }

        i=0
        for sekcja in p_dict['sekcje']:
            id_sekcji = 'sekcja_'+str(i)
            ilosc = sekcja['ilosc']
            formvaluedict.update({id_sekcji:ilosc})
            i+=1
        
        form = ProgramForm(formvaluedict);
        form.fields['nazwa_programu'].widget.attrs['readonly'] = True;
    return render(request, "SPO/program_form.html", {"form": form})

class AfkView(TemplateView):
    template_name = "SPO/afk.html";
