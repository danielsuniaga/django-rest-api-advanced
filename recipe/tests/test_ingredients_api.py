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

        Ingredient.objects.create(user=self.user, name='milk')

        Ingredient.objects.create(user=self.user, name='salt')

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')

        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_used(self):

        """ Probar retornar ingredientes solamente autenticados por el usuario """

        user2 = get_user_model().objects.create_user(

            'other@datadosis.com',

            'testpass'

        )

        Ingredient.objects.create(user=user2, name='Vinegar')

        ingredient = Ingredient.objects.create(user=self.user, name='tumeric')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(len(res.data), 1)

        self.assertEqual(res.data[0]['name'], ingredient.name)

    def test_create_ingredient_successful(self):

        """ Probar crear nuevo ingrediente """

        payload = {'name':'Chocolate'}

        self.client.post(INGREDIENTS_URL, payload)

        exists = Ingredient.objects.filter(

            user=self.user,

            name=payload['name']

        ).exists()

        self.assertTrue(exists)

    def test_create_ingredient_invalid(self):

        """  Crear ingrediente sin nada """

        payload = {'name':''}

        res = self.client.post(INGREDIENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)






