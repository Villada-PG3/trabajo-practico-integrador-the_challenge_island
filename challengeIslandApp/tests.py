from datetime import date

from django.test import TestCase
from django.urls import reverse

from .models import Desafio, Isla, Pais, Temporada

# Create your tests here.
class DesafiosViewTests(TestCase):
	@classmethod
	def setUpTestData(cls):
		pais = Pais.objects.create(nombre='Argentina', descripcion='Pais de prueba')
		isla = Isla.objects.create(nombre='Isla de prueba', pais=pais)
		cls.temporada_uno = Temporada.objects.create(
			nombre='Temporada Uno',
			isla=isla,
			fecha_inicio=date(2025, 1, 1),
			fecha_fin=date(2025, 2, 1),
		)
		cls.temporada_dos = Temporada.objects.create(
			nombre='Temporada Dos',
			isla=isla,
			fecha_inicio=date(2026, 1, 1),
			fecha_fin=date(2026, 2, 1),
		)
		Desafio.objects.create(
			temporada=cls.temporada_uno,
			nombre='Prueba mental',
			descripcion='Resolver el acertijo.',
			tipo=Desafio.TipoDesafio.MENTAL,
			puntos=100,
		)
		Desafio.objects.create(
			temporada=cls.temporada_dos,
			nombre='Prueba física',
			descripcion='Completar el recorrido.',
			tipo=Desafio.TipoDesafio.FISICA,
			recompensa='Ventaja',
		)

	def test_lists_challenges_from_all_seasons_by_default(self):
		response = self.client.get(reverse('desafios'))

		self.assertContains(response, 'Prueba mental')
		self.assertContains(response, 'Prueba física')
		self.assertContains(response, 'Todas las temporadas')

	def test_filters_challenges_by_season_id(self):
		response = self.client.get(
			reverse('desafios'),
			{'temporada_id': self.temporada_uno.id_temporada},
		)

		self.assertContains(response, 'Prueba mental')
		self.assertNotContains(response, 'Prueba física')
		self.assertContains(response, 'Temporada Uno')

	def test_invalid_season_id_falls_back_to_all_seasons(self):
		response = self.client.get(reverse('desafios'), {'temporada_id': 'no-valido'})

		self.assertContains(response, 'Prueba mental')
		self.assertContains(response, 'Prueba física')
