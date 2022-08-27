from rest_framework import viewsets, mixins, status

from rest_framework.authentication import TokenAuthentication

from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe

from recipe import serializers

from rest_framework.decorators import action

from rest_framework.response import Response

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
        
        """ Retorna clase de serializador apropiados """

        if self.action == 'retrieve':

            return serializers.RecipeDetailSerializer

        elif self.action == 'upload_image':

            return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        
        """ Crear un nuevo receta """

        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')

    def upload_imagen(self, request, pk=None):

        """ Subir imagenes a recetas """

        recipe = self.get_object()

        serializer = self.get_serializer(

            recipe,

            data = request.data

        )

        if serializer.is_valid():

            serializer.save()

            return Response(

                serializer.data,

                status=status.HTTP_200_OK

            )

        return Response(

            serializer.errors,

            status=status.HTTP_400_BAD_REQUEST

        )