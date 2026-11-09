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
            super().get_queryset()
            .select_related('isla', 'isla__pais')
            .prefetch_related(
                'equipos',
                'equipos__detalles_alianzas__alianza'
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        temporada = self.object

        equipos = list(temporada.equipos.all())

        eliminaciones = (
            Eliminacion.objects
            .filter(equipo_eliminado__temporada=temporada)
            .select_related('equipo_eliminado', 'tipo')
            .order_by('tipo__numero', 'id_eliminacion')
        )

        eliminaciones_por_numero = {}

        for eliminacion in eliminaciones:
            eliminaciones_por_numero.setdefault(
                eliminacion.tipo.numero,
                eliminacion.equipo_eliminado
            )

        equipos_piramide = []

        for equipo in equipos:
            alianzas_temporada = [
                detalle
                for detalle in equipo.detalles_alianzas.all()
                if (
                    detalle.fecha_inicio <= temporada.fecha_fin
                    and (
                        detalle.fecha_fin is None
                        or detalle.fecha_fin >= temporada.fecha_inicio
                    )
                )
            ]

            alianza = max(
                alianzas_temporada,
                key=lambda detalle: detalle.fecha_inicio,
                default=None
            )

            equipos_piramide.append({
                'equipo': equipo,
                'color_alianza': (
                    alianza.alianza.color if alianza else None
                ),
            })

        niveles_piramide = []

        for numero in range(1, len(equipos)):
            equipo_eliminado = eliminaciones_por_numero.get(numero)

            equipos_que_siguen = []

            for item in equipos_piramide:
                equipo = item['equipo']

                eliminacion_equipo = next(
                    (
                        eliminacion
                        for eliminacion in eliminaciones
                        if eliminacion.equipo_eliminado_id == equipo.pk
                    ),
                    None
                )

                if (
                    eliminacion_equipo is None
                    or eliminacion_equipo.tipo.numero > numero
                ):
                    equipos_que_siguen.append(item)

            cantidad_esperada = len(equipos) - numero

            lugares_desconocidos = max(
                0,
                cantidad_esperada - len(equipos_que_siguen)
            )

            niveles_piramide.append({
                'numero': numero,
                'eliminado': equipo_eliminado,
                'equipos': equipos_que_siguen,
                'lugares_desconocidos': range(lugares_desconocidos),
            })

        campeon = next(
            (equipo for equipo in equipos if equipo.es_ganador),
            None
        )

        context['equipos_piramide'] = equipos_piramide
        context['niveles_piramide'] = niveles_piramide
        context['campeon'] = campeon

        return context

class DetalleEquipoView(DetailView):
    model = Equipo
    template_name = 'detalle_equipo.html'
    context_object_name = 'equipo'

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related('temporada')
            .prefetch_related('participantes__pais')
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


class DesafiosView(ListView):
    model = Desafio
    template_name = 'desafios.html'
    context_object_name = 'desafios'

    def get_queryset(self):
        queryset = Desafio.objects.select_related('temporada').order_by(
            '-temporada__fecha_inicio', 'nombre'
        )
        temporada_id = self.request.GET.get('temporada_id', '').strip()
        self.temporada_seleccionada = None

        if temporada_id.isdigit():
            self.temporada_seleccionada = Temporada.objects.filter(
                pk=temporada_id
            ).first()
            if self.temporada_seleccionada:
                queryset = queryset.filter(temporada=self.temporada_seleccionada)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['temporadas'] = Temporada.objects.order_by(
            '-fecha_inicio', '-id_temporada'
        )
        context['temporada_seleccionada'] = self.temporada_seleccionada
        return context