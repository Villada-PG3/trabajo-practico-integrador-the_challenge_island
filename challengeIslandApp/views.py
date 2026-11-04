from django.shortcuts import render
from django.views.generic import DetailView, TemplateView
from .models import Temporada
# Create your views here.
class home(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['temporada_actual'] = Temporada.objects.select_related(
            'isla', 'isla__pais'
        ).order_by('-fecha_inicio', '-id_temporada').first()
        return context


class TemporadasView(TemplateView):
    template_name = 'temporadas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['temporadas'] = Temporada.objects.select_related(
            'isla'
        ).order_by('-fecha_inicio', '-id_temporada')
        return context


class DetalleTemporadaView(DetailView):
    model = Temporada
    template_name = 'detalle_temporada.html'
    context_object_name = 'temporada'

    def get_queryset(self):
        return super().get_queryset().select_related('isla', 'isla__pais')