from django.contrib.auth import get_user_model

from django.urls import reverse

from django.test import TestCase

from rest_framework import status

from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipe:ingredient-list')

class PublicIngredientsApiTest(TestCase):

    """ Probar API de ingredients accesibles publicamente """

    def setUp(self):

        self.client = APIClient()

    def test_login_required(self):

        """ Probar que login es necesario para acceder al endpoint """

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateIngredientsApiTest(TestCase):

    """ Probar API de ingredients accesibles privadamente """

    def setUp(self):

        self.client = APIClient()

        self.user = get_user_model().objects.create_user(

            'test@datadosis.com',

            'testpass'

        )

        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient_list(self):

        """ Probar obtener lista de ingredientes """