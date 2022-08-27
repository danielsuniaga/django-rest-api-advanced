from django.test import TestCase

from django.contrib.auth import get_user_model

from unittest.mock import patch

from core import models

def sample_user(email='test@datadosiscom', password='testpass'):

    """ Crear usuario ejemplo """

    return get_user_model().objects.create_user(email, password)

class ModelText(TestCase):

    def test_create_user_with_email_successful(self):

        """ Probar crear un nuevo usuario con un email correctamente """

        email= 'test@datadosis.com'

        password = 'Testpass123'

        user = get_user_model().objects.create_user(

            email = email,

            password = password

        )

        self.assertEqual(user.email, email)

        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):

        """ Testear email para nuevo usuario normalizado """

        email = 'test@DATADOSIS.COM'

        user = get_user_model().objects.create_user(
            email,
            'Testpass123'
        )

        self.assertEqual(user.email, email.lower())

    def text_new_user_invalid_email(self):

        """Nuevo usuario email invalido"""

        with self.assertRaises(ValueError):

            user = get_user_model().objects.create_user(
                None,
                'Testpass123'
            )

    def test_create_new_superuser(self):

        """ Probar superusuario creado """

        email= 'test@datadosis.com'

        password = 'Testpass123'

        user = get_user_model().objects.create_super_user(

            email = email,

            password = password

        )

        self.assertTrue(user.is_superuser)

        self.assertTrue(user.is_staff)

    def test_tag_str(self):

        """ Probar representación en cadena de texto del tags """

        tag = models.Tag.objects.create(

            user = sample_user(),

            name = 'Meat'

        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):

        """ Probar representación en cadena de texto del ingrediente """

        ingredient = models.Ingredient.objects.create(

            user = sample_user(),

            name = 'Banana'

        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):

        """  probar representaciones en cadena de texto del recetas """

        recipe = models.Recipe.objects.create(

            user=sample_user(),

            title = 'Steak and mushroom souce',

            time_minutes = 5,

            price=5.00

        )

        self.assertEqual(str(recipe), recipe.title)
