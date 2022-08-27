from rest_framework import viewsets, mixins

from rest_framework.authentication import TokenAuthentication

from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe

from recipe import serializers

# Create your views here.

class BaseRecipeAttrViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):

    """ Viewsets base """

    authentication_classes = (TokenAuthentication,)

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):

        """ Retornar objetos para el usurio autenticado """

        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        
        """ Crear un nuevo Tag """

        serializer.save(user=self.request.user)

class TagViewSet(BaseRecipeAttrViewSet):

    """ Manejar Tags en base de datos """

    queryset = Tag.objects.all()

    serializer_class = serializers.TagSerializer



class IngredientViewSet(BaseRecipeAttrViewSet):

    """ Manejar ingredientes en base de datos """

    queryset = Ingredient.objects.all()

    serializer_class = serializers.IngredientSerializer

class RecipeViewSet(viewsets.ModelViewSet):

    """ Maneja recetas en base de datos """

    serializer_class = serializers.RecipeSerializer

    queryset = Recipe.objects.all()

    authentication_classes = (TokenAuthentication,)

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):

        """ Retornar objetos para el usurio autenticado """

        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        
        """ Retorna clase de serializador apropiaos """

        if self.action == 'retrieve':

            return serializers.RecipeDetailSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        
        """ Crear un nuevo receta """

        serializer.save(user=self.request.user)
