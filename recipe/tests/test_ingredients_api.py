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