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
from plan_podlewania import plan_podlewania
from komunikator import *

discord = None;

class ZaworyView(ListView):
    model = Zawor
    template_name = 'SPO/zawory.html'

    def get_context_data(self, **kwargs):
        from tester_komunikatora2 import tester
        global discord;
        if(discord == None):
            discord = komunikator(config.port_do_komunikacji);
            discord.polacz();
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
        programy=[]
        try:
            with open("plan_programow.txt", "r") as f:
                for l in f:
                    program = l.strip().split("|")
                    programy.append(program)
                    program[3]=eval(program[3])
                    program[4]=eval(program[4])
        except FileNotFoundError:
            pass
        context["plan"] = programy
        return context
    
def ProgramRemoveView(request, program_name):

    print("Want to remove:",program_name) #Tu funkcja usuwania
    discord.wyslij(kod_komunikatu.USUN_PROGRAM, program_name);
    return redirect('zawory')

def ProgramCreateView(request):
    if request.method == "POST":
        form = ProgramForm(request.POST)
        if form.is_valid():

            print("Want to create:",form.cleaned_data) #Tu funkcja dodawania

            return redirect('zawory')
    else:
        valuedict={}
        for i in config.rozpiska_sekcji:
            valuedict.update({f'sekcja_{i}':0.0})
        form = ProgramForm(valuedict)
    return render(request, "SPO/program_form.html", {"form": form})

def ProgramEditView(request, program_name):
    if request.method == "POST":
        form = ProgramForm(request.POST)
        form.fields['nazwa_programu'].widget.attrs['readonly'] = True
        if form.is_valid():

            print("Want to edit:",form.cleaned_data) #Tu funkcja edycji

            return redirect('zawory')
    else:
        #LOAD JSON HERE TO GET DATA FROM PROGRAM
        valuedict={'nazwa_programu':program_name}

        form = ProgramForm(valuedict)
        form.fields['nazwa_programu'].widget.attrs['readonly'] = True
    return render(request, "SPO/program_form.html", {"form": form})
