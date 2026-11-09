from django.contrib import admin
from django.utils.html import format_html

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

admin.site.site_header = "THE CHALLENGE ISLAND"
admin.site.site_title = "The Challenge Island | Administración"
admin.site.index_title = "Panel de administración"


class ImagePreviewAdmin(admin.ModelAdmin):
    readonly_fields = ("imagen_preview",)

    @admin.display(description="Vista previa")
    def imagen_preview(self, obj):
        if obj is None or not obj.imagen:
            return format_html(
                '<div class="admin-image-preview">'
                '<span class="admin-image-preview__empty">{}</span>'
                "</div>",
                "La vista previa estará disponible después de guardar.",
            )
        return format_html(
            '<div class="admin-image-preview">'
            '<img class="admin-image-preview__image" src="{}" alt="Imagen de {}">'
            "</div>",
            obj.imagen.url,
            obj,
        )

    def get_fields(self, request, obj=None):
        fields = list(super().get_fields(request, obj))
        if "imagen" in fields and "imagen_preview" in fields:
            fields.remove("imagen_preview")
            fields.insert(fields.index("imagen") + 1, "imagen_preview")
        return fields


admin.site.register((Equipo, Pais, Participante, Temporada), ImagePreviewAdmin)
admin.site.register(
    (
        Alianza,
        AmbitoVida,
        HabilidadEspecial,
        Stat,
        TipoEliminacion,
        Isla,
        ConjuntoStat,
        Desafio,
        Eliminacion,
        DetalleAlianza,
        DetalleHabilidadEspecial,
        DetalleAmbitoVida,
        DetalleConjunto,
        SuperadorDesafio,
    )
)
