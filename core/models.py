from email.policy import default
from turtle import Turtle
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from django.conf import settings
# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):

         """ Crea y guarda un nuevo Usuario"""

         if not email:

            raise ValueError('User not have an email')

         user = self.model(email=self.normalize_email(email), **extra_fields)

         user.set_password(password)

         user.save(using=self._db)

         return user

    def create_super_user(self, email, password):

        """Crear superusuario"""

        user=self.create_user(email, password)

        user.is_staff = True

        user.is_superuser = True

        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):

    """ Modelo personalizado de Usuario que soporta hacer login con Email en vez de usuario """

    email = models.EmailField(max_length=255, unique=True)

    name = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

class Tag(models.Model):

    """ Modelo del tag para la receta """

    name = models.CharField(max_length=255)

    user = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE

    )

    def __str__(self):
        
        return self.name

class Ingredient(models.Model):

    """ Ingrediente para usar en la receta """

    name = models.CharField(max_length=255)

    user = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE

    )

    def __str__(self):
        
        return self.name




