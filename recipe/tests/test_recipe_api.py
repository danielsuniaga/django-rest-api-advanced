from xmlrpc.client import APPLICATION_ERROR
from django.contrib.auth import get_user_model

from django.test import TestCase

from django.urls import reverse

from rest_framework import status

from rest_framework.test import APIClient

from core.models import Recipe, Tag, Ingredient

from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

import tempfile

import os

from PIL import Image

RECIPES_URL = reverse('recipe:recipe-list')

def image_upload_url(recipe_id):

    """ URL de retorno para imagen publica """

    return reverse('recipe:recipe-upload-image', args=[recipe_id])

def sample_tag(user, name='Main course'):

    """ Crear un tag ejemplo """

    return Tag.objects.create(user=user, name=name)

def sample_ingredient(user, name='Cinnamon'):

    """ Crear un ingrediente ejemplo """

    return Ingredient.objects.create(user=user, name=name)

def detail_url(recipe_id):

    """ Retorna Receta detail URL """

    return reverse('recipe:recipe-detail', args=[recipe_id])

def sample_recipe (user, **params):

    """ Crear y retornar receta """

    defaults = {

        'title': 'Sample recipe',

        'time_minutes':10,

        'price':5.00,

    }

    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)

class PublicRecipeApiTests(TestCase):

    """ Test acceso no autenticado API """

    def setUp(self):

        self.client = APIClient()

        self.user = get_user_model().objects.create_user(

            'test@datadosis.com',

            'testpass'

        )

        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):

        """ Probar obtener lista de recetas """

        sample_recipe(user=self.user)

        sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('id')

        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_to_user(self):

        """ Probar obtener receta para un usuario """

        user2 = get_user_model().objects.create_user(

            'other@datadosis.com',

            'pass'

        )

        sample_recipe(user=user2)

        sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user)

        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(len(res.data), 1)

        self.assertEqual(res.data, serializer.data)

    def test_view_recipe_detail(self):

        recipe = sample_recipe(user=self.user)

        recipe.tags.add(sample_tag(user=self.user))

        recipe.ingredients.add(sample_ingredient(user=self.user))

        url =detail_url(recipe.id)

        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)

        self.assertEqual(res.data, serializer.data)

    def test_create_basic_recipe(self):

        """ Probar crear receta """

        payload = {

            'title':'Test recipe',

            'time_minutes': 30,

            'price': 10.00,

        }

        res = self.client.post(RECIPES_URL, payload)

        recipe = Recipe.objects.get(id=res.data['id'])

        for key in payload.keys():

            self.assertEqual(payload[key], getattr(recipe, key))

    def test_create_recipe_with_tags(self):

        """ Prueba crear receta con tags """

        tag1 = sample_tag(user=self.user, name='Tag 1')

        tag2 = sample_tag(user=self.user, name='Tag 2')

        payload = {

            'title': 'Test recipe with tow tag',

            'tags': [tag1.id, tag2.id],

            'time_minutes': 30,

            'price': 10.00

        }

        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(id=res.data['id'])

        tags = recipe.tags.all()

        self.assertEqual(tags.count(), 2)

        self.assertIn(tag1, tags)

        self.assertIn(tag2, tags)


 
class RecipeImageUploadTests(TestCase):

    """ Test para gestión de imagenes asociadas a recipes """

    def setUp(self):

        self.client = APIClient()

        self.user = get_user_model().objects.create_user('user','testpass')

        self.client.force_authenticate(self.user)

        self.recipe = sample_recipe(user=self.user)

    def tearDown(self):

        self.recipe.image.delete()

    
        
