from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView, View
from django.urls import reverse_lazy
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from .models import Zawor, Wodomierz, HistoriaZdarzen # Dodano import HistoriaZdarzen
from .forms import ZaworForm, ONOFF # Użyte w komentarzach, zostawiam
from django.views import generic # Użyte w komentarzach, zostawiam
from hardware import sekcje # Użyte w pierwszym fragmencie
from konfiguracja import config # Zmieniono na config aby pasowało do użycia

# Zakładam, że importujesz config jako 'config' a nie za pomocą 'from konfiguracja import *'
# Jeśli 'konfiguracja' to plik, z którego importujesz 'config', to:
# from konfiguracja import config 

test_value=0

# Klasa ZaworyView (ListView) - Wyświetlanie listy zaworów
class ZaworyView(ListView):
    model = Zawor
    template_name = 'SPO/zawory.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Zawor.objects.order_by("real_id")
        # Poprawka: Django zaleca używanie 'queryset' w ListView, 
        # ale użycie get_context_data jest poprawne dla dodatkowych danych
        context["zawory"] = Zawor.objects.all().order_by("real_id") 
        return context

# Klasa ZaworCreateView (CreateView) - Tworzenie nowego zaworu
class ZaworCreateView(CreateView):
    model = Zawor
    fields = ['name', 'status']
    template_name = 'SPO/zawor_form.html'
    success_url = reverse_lazy('zawory')

# Funkcja ZaworONOFFView - Przełączanie statusu zaworu
def ZaworONOFFView(request, zawor_id):
    zawor = get_object_or_404(Zawor, id=zawor_id)
    if request.method == "POST":
        # Logika przełączania statusu
        zawor.status = not zawor.status
        # if zawor.status == True:
        #     zawor.status = False
        # else:
        #     zawor.status = True
        
        # Opcjonalnie: logowanie zdarzenia, np. do HistoriaZdarzen
        # HistoriaZdarzen.dodaj_zdarzenie(f"Zmieniono status zaworu ID {zawor_id} na {zawor.status}")

        zawor.save()
        return redirect('zawory')

# Klasa WodomierzView (TemplateView) - Wyświetlanie statusu wodomierza
class WodomierzView(TemplateView):
    template_name = "SPO/wodomierz.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Wodomierz.objects.get(pk=1).ilosc
        # Zakładam, że 'ilosc' przechowuje liczbę sygnałów
        try:
            wodomierz = Wodomierz.objects.get(pk=1)
            sygnaly = wodomierz.ilosc
            # Zastosowanie config.ilosc_wody_na_sygnal
            context["wodomierz_status"] = float(sygnaly) * config.ilosc_wody_na_sygnal
        except Wodomierz.DoesNotExist:
            context["wodomierz_status"] = "Brak danych wodomierza"
        except NameError: # W przypadku braku importu 'config'
            context["wodomierz_status"] = "Błąd konfiguracji (brak config)"
        
        return context

# Funkcja historia_zdarzen_view - Wyświetlanie historii zdarzeń (Singleton)
def historia_zdarzen_view(request):
    # Używamy statycznej metody do pobrania listy z pamięci Singletonu
    logi = HistoriaZdarzen.pobierz_historie()
    context = {
        'logi': logi,
        'tytul': 'Historia Zdarzeń Systemu (Pamięć)'
    }
    return render(request, 'SPO/historia_zdarzen.html', context)

# --- Usunięte/Zakomentowane nieużywane fragmenty dla czystości ---
# test_value = 0
# ZAWOR_DATA = [...]
# Zakomentowane widoki oparte na TemplateView
