from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe

from recipe import serializers


class BaseRecipeAttViewSet(viewsets.GenericViewSet,
                           mixins.ListModelMixin,
                           mixins.CreateModelMixin):
        """Base viewset for user owned recipe atrubutes"""
        authentication_classes = (TokenAuthentication,)
        permission_classes = (IsAuthenticated,)

        def get_queryset(self):
            """Return obkect for the current authenticate user only"""
            return self.queryset.filter(
                user=self.request.user).order_by('-name')

        def perform_create(self, serializer):
            """Create a new object"""
            serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttViewSet):
    """Manage tags in the database"""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipeAttViewSet):
    """Manage ingrediets in the database"""
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve the recipes for the authenticated user"""
        return self.queryset.filter(user=self.request.user)
