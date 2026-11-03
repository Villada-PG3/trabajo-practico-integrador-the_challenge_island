from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import UniqueConstraint


# =====================================================
# GEOGRAFIA
# =====================================================

class Pais(models.Model):
    id_pais = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(
        upload_to='paises/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.nombre


class Isla(models.Model):
    id_isla = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    pais = models.ForeignKey(
        Pais,
        on_delete=models.PROTECT,
        related_name='islas'
    )

    def __str__(self):
        return self.nombre


# =====================================================
# TEMPORADAS
# =====================================================

class Temporada(models.Model):
    id_temporada = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    isla = models.ForeignKey(
        Isla,
        on_delete=models.PROTECT,
        related_name='temporadas'
    )
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def clean(self):
        if self.fecha_fin < self.fecha_inicio:
            raise ValidationError(
                'La fecha de finalización no puede ser anterior '
                'a la fecha de inicio.'
            )

    def __str__(self):
        return self.nombre


# =====================================================
# EQUIPOS
# =====================================================

class Equipo(models.Model):
    id_equipo = models.AutoField(primary_key=True)
    temporada = models.ForeignKey(
        Temporada,
        on_delete=models.PROTECT,
        related_name='equipos'
    )
    activo = models.BooleanField(default=True)
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(
        upload_to='equipos/',
        blank=True,
        null=True
    )
    puntaje = models.PositiveIntegerField(default=0)
    es_ganador = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre


# =====================================================
# PARTICIPANTES
# =====================================================

class Participante(models.Model):
    id_participante = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    apodo = models.CharField(max_length=100)
    edad = models.PositiveIntegerField()
    pais = models.ForeignKey(
        Pais,
        on_delete=models.PROTECT,
        related_name='participantes'
    )
    equipo = models.ForeignKey(
        Equipo,
        on_delete=models.PROTECT,
        related_name='participantes'
    )
    imagen = models.ImageField(
        upload_to='participantes/',
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.nombre} {self.apellido}'


# =====================================================
# ALIANZAS
# =====================================================

class Alianza(models.Model):
    id_alianza = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class DetalleAlianza(models.Model):
    id_detalle_alianza = models.AutoField(primary_key=True)
    equipo = models.ForeignKey(
        Equipo,
        on_delete=models.PROTECT,
        related_name='detalles_alianzas'
    )
    alianza = models.ForeignKey(
        Alianza,
        on_delete=models.PROTECT,
        related_name='detalles_alianzas'
    )
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(
        blank=True,
        null=True
    )
    estado = models.BooleanField(default=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['equipo', 'alianza'],
                name='unique_equipo_alianza'
            )
        ]

    def clean(self):
        if (
            self.fecha_fin is not None
            and self.fecha_fin < self.fecha_inicio
        ):
            raise ValidationError(
                'La fecha de finalización no puede ser anterior '
                'a la fecha de inicio.'
            )

    def __str__(self):
        return f'{self.equipo} - {self.alianza}'


# =====================================================
# AMBITOS DE VIDA
# =====================================================

class AmbitoVida(models.Model):
    id_ambito_vida = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=150)

    def __str__(self):
        return self.descripcion


class DetalleAmbitoVida(models.Model):
    id_detalle_ambito_vida = models.AutoField(primary_key=True)
    participante = models.ForeignKey(
        Participante,
        on_delete=models.CASCADE,
        related_name='detalles_ambitos'
    )
    ambito_vida = models.ForeignKey(
        AmbitoVida,
        on_delete=models.PROTECT,
        related_name='detalles_participantes'
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['participante', 'ambito_vida'],
                name='unique_participante_ambito'
            )
        ]

    def __str__(self):
        return f'{self.participante} - {self.ambito_vida}'


# =====================================================
# HABILIDADES ESPECIALES
# =====================================================

class HabilidadEspecial(models.Model):
    id_habilidad_especial = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=150)

    def __str__(self):
        return self.descripcion


class DetalleHabilidadEspecial(models.Model):
    id_detalle_habilidad_especial = models.AutoField(primary_key=True)
    participante = models.ForeignKey(
        Participante,
        on_delete=models.CASCADE,
        related_name='detalles_habilidades'
    )
    habilidad_especial = models.ForeignKey(
        HabilidadEspecial,
        on_delete=models.PROTECT,
        related_name='detalles_participantes'
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['participante', 'habilidad_especial'],
                name='unique_participante_habilidad'
            )
        ]

    def __str__(self):
        return f'{self.participante} - {self.habilidad_especial}'


# =====================================================
# ESTADISTICAS
# =====================================================

class ConjuntoStat(models.Model):
    id_conjunto_stat = models.AutoField(primary_key=True)
    fecha_creacion = models.DateField()
    participante = models.ForeignKey(
        Participante,
        on_delete=models.CASCADE,
        related_name='conjuntos_stats'
    )

    def __str__(self):
        return f'Estadísticas de {self.participante}'


class Stat(models.Model):
    id_stat = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre


class DetalleConjunto(models.Model):
    id_detalle_conjunto = models.AutoField(primary_key=True)
    stat = models.ForeignKey(
        Stat,
        on_delete=models.PROTECT,
        related_name='detalles_conjuntos'
    )
    conjunto_stat = models.ForeignKey(
        ConjuntoStat,
        on_delete=models.CASCADE,
        related_name='detalles'
    )
    cantidad = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['stat', 'conjunto_stat'],
                name='unique_stat_conjunto'
            )
        ]

    def __str__(self):
        return f'{self.stat} - {self.cantidad}'


# =====================================================
# ELIMINACIONES
# =====================================================

class TipoEliminacion(models.Model):
    id_tipo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre


class Eliminacion(models.Model):
    id_eliminacion = models.AutoField(primary_key=True)
    equipo_eliminado = models.ForeignKey(
        Equipo,
        on_delete=models.PROTECT,
        related_name='eliminaciones'
    )
    tipo = models.ForeignKey(
        TipoEliminacion,
        on_delete=models.PROTECT,
        related_name='eliminaciones'
    )
    descripcion = models.TextField()

    def __str__(self):
        return f'Eliminación de {self.equipo_eliminado}'


# =====================================================
# DESAFIOS
# =====================================================

class Desafio(models.Model):
    id_desafio = models.AutoField(primary_key=True)
    temporada = models.ForeignKey(
        Temporada,
        on_delete=models.PROTECT,
        related_name='desafios'
    )
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    puntos = models.PositiveIntegerField(default=0)
    recompensa = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre


class SuperadorDesafio(models.Model):
    id_superador = models.AutoField(primary_key=True)
    desafio = models.ForeignKey(
        Desafio,
        on_delete=models.CASCADE,
        related_name='superadores'
    )
    equipo = models.ForeignKey(
        Equipo,
        on_delete=models.PROTECT,
        related_name='desafios_superados'
    )
    puntaje_obtenido = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['desafio', 'equipo'],
                name='unique_equipo_desafio'
            )
        ]

    def __str__(self):
        return f'{self.equipo} - {self.desafio}'
