from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Temporada
# Create your views here.
class home(TemplateView):
    template_name = 'home.html'


class TemporadasView(TemplateView):
    template_name = 'temporadas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['temporadas'] = Temporada.objects.select_related(
            'isla'
        ).order_by('-fecha_inicio', '-id_temporada')
        return context