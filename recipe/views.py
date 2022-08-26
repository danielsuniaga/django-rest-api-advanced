from rest_framework import viewsets, mixins

from rest_framework.authentication import TokenAuthentication

from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient

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

