
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home.as_view(), name="home"),
    path("home/", views.home.as_view(), name="home_alias"),
    path("temporadas/", views.TemporadasView.as_view(), name="temporadas"),
    path("desafios/", views.DesafiosView.as_view(), name="desafios"),
    path(
        "temporada/<int:pk>/",
        views.DetalleTemporadaView.as_view(),
        name="detalle_temporada",),
    path(
            'participantes/',
            views.ParticipantesView.as_view(),
            name='participantes'),
    path(
            'participante/<int:pk>/',
            views.DetalleParticipanteView.as_view(),
            name='detalle_participante'
        ),
]
