from rest_framework import serializers

from core.models import Tag, Ingredient, Recipe

class TagSerializer(serializers.ModelSerializer):

    """ Serializador para objeto de tags """

    class Meta: 

        model = Tag

        fields = ('id', 'name')

        read_only_Fields = ('id',)

class IngredientSerializer(serializers.ModelSerializer):

    """ Serializador para objeto de ingrediente """

    class Meta: 

        model = Ingredient

        fields = ('id', 'name')

        read_only_Fields = ('id',)

class RecipeSerializer(serializers.ModelSerializer):

    """ Serializador recetas """

    ingredients = serializers.PrimaryKeyRelatedField(

        many = True,

        queryset = Ingredient.objects.all()

    )

    tags = serializers.PrimaryKeyRelatedField(

        many = True,

        queryset = Tag.objects.all()

    )

    class Meta:

        model = Recipe

        fields = (

            'id', 'title', 'ingredients','tags', 'time_minutes','price', 'link',

        )

        read_only_fieds = {'id',}

class RecipeDetailSerializer(RecipeSerializer):

    """ Serializar detalle de Receta """

    ingredients = IngredientSerializer(many=True, read_only=True)

    tags = TagSerializer(many=True, read_only=True)