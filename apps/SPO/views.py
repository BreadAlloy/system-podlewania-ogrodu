from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from .models import Zawor
from .forms import ZaworForm, ONOFF
from django.views import generic


ZAWOR_DATA = [
    {'id': '0', 'name': 'Rainbird', 'status': 'ON'},
    {'id': '1', 'name': 'Hunter', 'status': 'OFF'},
    {'id': '2', 'name': '1/2 I Quot 3/4 I Quot 1 Cal Elektrozawór Do Nawadniania 12V/24VAC Elektrozawory Ogród Rolnictwo Architektura Krajobrazu Elektrozawór Do Nawadniania (Color : 1", Size : DC Latching(9-20V)) ', 'status': 'ON'},
]

#class ZaworyView(generic.TemplateView):
#    template_name = "SPO/zawory.html"
#
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context["zawory"] = ZAWOR_DATA
#        return context

class ZaworyView(ListView):
    model = Zawor
    template_name = 'SPO/zawory.html'


class ZaworCreateView(CreateView):
    model = Zawor
    fields = ['name', 'status']
    template_name = 'SPO/zawor_form.html'
    success_url = reverse_lazy('zawory')

    #def form_valid(self, form):
        # np. gdy byśmy chcieli ustawiać autora na zalogowanego usera: form.instance.author = self.request.user
    #    return super().form_valid(form)

#class ZaworONOFFView(TemplateView):
#    template_name = 'SPO/ONOFF.html'
#
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        pkreal=Zawor.objects.get(pk=1)
#        context['form'] = ONOFF(instance=pkreal)
#        return context
#
#    def post(self, request, *args, **kwargs):
#        pkreal=Zawor.objects.get(pk=1)
#        form = ONOFF(request.POST, instance=pkreal)
#        if form.is_valid():
#            new_zawor = form.save()
#
#            return redirect(reverse_lazy("zawory"))
#
#        context = self.get_context_data(**kwargs)
#        context['form'] = form
#        return self.render_to_response(context)

def ZaworONOFFView(request, zawor_id):
    zawor=get_object_or_404(Zawor, id=zawor_id)
    if request.method == "POST":
        if zawor.status=='OFF':
            zawor.status='ON'
        else:
            zawor.status='OFF'
        zawor.save()
        return redirect('zawory')

