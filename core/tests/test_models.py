from django.test import TestCase

from django.contrib.auth import get_user_model

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
