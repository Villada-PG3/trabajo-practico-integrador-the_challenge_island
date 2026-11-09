from datetime import date

from django.apps import apps
from django.contrib.auth import get_user_model
from django.db.models import ImageField
from django.test import TestCase
from django.urls import reverse

from .models import Desafio, Isla, Pais, Temporada

# Create your tests here.
class AdminImagePreviewTests(TestCase):
	@classmethod
	def setUpTestData(cls):
		cls.admin_user = get_user_model().objects.create_superuser(
			username='admin',
			email='admin@example.com',
			password='test-password',
		)
		cls.pais = Pais.objects.create(
			nombre='Argentina',
			descripcion='Pais de prueba',
			imagen='paises/argentina.jpg',
		)

	def setUp(self):
		self.client.force_login(self.admin_user)

	def test_admin_dashboard_shows_model_actions_and_recent_activity(self):
		response = self.client.get(reverse('admin:index'))

		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'admin/index.html')
		self.assertContains(response, 'Centro de gestión')
		self.assertContains(response, 'Acciones recientes')
		self.assertContains(
			response,
			reverse(
				f'admin:{Temporada._meta.app_label}_{Temporada._meta.model_name}_changelist'
			),
		)
		self.assertContains(
			response,
			reverse(
				f'admin:{Temporada._meta.app_label}_{Temporada._meta.model_name}_add'
			),
		)

	def test_add_form_includes_preview_notice_and_shared_styles(self):
		url = reverse(
			f'admin:{Pais._meta.app_label}_{Pais._meta.model_name}_add'
		)
		response = self.client.get(url)

		self.assertContains(response, 'La vista previa estará disponible después de guardar')
		self.assertNotContains(response, 'admin_image_preview.js')
		self.assertContains(response, 'css/estilos.css')
		self.assertContains(response, 'bootstrap@5.3.3')

	def test_change_form_displays_saved_image_preview(self):
		url = reverse(
			f'admin:{Pais._meta.app_label}_{Pais._meta.model_name}_change',
			args=(self.pais.pk,),
		)
		response = self.client.get(url)

		self.assertContains(response, 'src="/media/paises/argentina.jpg"')
		self.assertContains(response, 'admin-image-preview__image')

	def test_only_the_four_requested_models_have_image_fields(self):
		image_fields = {
			model.__name__: field
			for model in apps.get_app_config('challengeIslandApp').get_models()
			for field in model._meta.get_fields()
			if isinstance(field, ImageField)
		}

		self.assertEqual(
			set(image_fields),
			{'Pais', 'Temporada', 'Equipo', 'Participante'},
		)
		self.assertEqual(image_fields['Pais'].upload_to, 'paises/')
		self.assertEqual(image_fields['Temporada'].upload_to, 'temporadas/')
		self.assertEqual(image_fields['Equipo'].upload_to, 'equipos/')
		self.assertEqual(image_fields['Participante'].upload_to, 'participantes/')


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
