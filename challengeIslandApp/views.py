from django.shortcuts import render
from django.views.generic import DetailView, TemplateView, ListView
from .models import *
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
        return (
            super()
            .get_queryset()
            .select_related('isla', 'isla__pais')
            .prefetch_related('equipos')
        )
class ParticipantesView(ListView):
    model = Participante
    template_name = 'participantes.html'
    context_object_name = 'participantes'

    def get_queryset(self):
        return (
            Participante.objects
            .select_related('pais', 'equipo', 'equipo__temporada')
            .order_by('apellido', 'nombre')
        )


class DetalleParticipanteView(DetailView):
    model = Participante
    template_name = 'detalle_participante.html'
    context_object_name = 'participante'

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related(
                'pais',
                'equipo',
                'equipo__temporada',
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        conjunto = self.object.conjuntos_stats.order_by(
            '-fecha_creacion',
            '-id_conjunto_stat'
        ).first()

        if conjunto:
            detalles = conjunto.detalles.select_related('stat').all()

            estadisticas = [
                {
                    'nombre': detalle.stat.nombre,
                    'descripcion': detalle.stat.descripcion,
                    'cantidad': detalle.cantidad,
                    'porcentaje': detalle.cantidad,
                }
                for detalle in detalles
            ]
        else:
            estadisticas = []

        context['estadisticas'] = estadisticas

        return context