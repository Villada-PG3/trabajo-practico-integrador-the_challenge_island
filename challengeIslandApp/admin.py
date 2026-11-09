from django.contrib import admin

admin.site.site_header = "THE CHALLENGE ISLAND"
admin.site.site_title = "The Challenge Island | Administración"
admin.site.index_title = "Panel de administración"

from .models import (
    Alianza,
    AmbitoVida,
    Equipo,
    HabilidadEspecial,
    Pais,
    Stat,
    TipoEliminacion,
    Isla,
    Participante,
    ConjuntoStat,
    Temporada,
    Desafio,
    Eliminacion,
    DetalleAlianza,
    DetalleHabilidadEspecial,
    DetalleAmbitoVida,
    DetalleConjunto,
    SuperadorDesafio,
)

admin.site.register(Alianza)
admin.site.register(AmbitoVida)
admin.site.register(Equipo)
admin.site.register(HabilidadEspecial)
admin.site.register(Pais)
admin.site.register(Stat)
admin.site.register(TipoEliminacion)
admin.site.register(Isla)
admin.site.register(Participante)
admin.site.register(ConjuntoStat)
admin.site.register(Temporada)
admin.site.register(Desafio)
admin.site.register(Eliminacion)
admin.site.register(DetalleAlianza)
admin.site.register(DetalleHabilidadEspecial)
admin.site.register(DetalleAmbitoVida)
admin.site.register(DetalleConjunto)
admin.site.register(SuperadorDesafio)
