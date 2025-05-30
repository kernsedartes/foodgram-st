from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.validators import UniqueTogetherValidator
from djoser.serializers import TokenCreateSerializer
from .models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
)
from users.models import Subscription, User
from django.contrib.auth import authenticate
from api.utils import Base64ImageField

MIN_AMOUNT = 1
MAX_AMOUNT = 32000
MAX_NAME_LENGTH = 256
MIN_TEXT_LENGTH = 1


class CustomTokenCreateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(
            email=attrs.get("email"), password=attrs.get("password")
        )

        if not user:
            raise serializers.ValidationError(
                {"auth_token": ["Неверные учетные данные"]}
            )

        self.user = user

        refresh = RefreshToken.for_user(user)
        return {
            "auth_token": str(refresh.access_token),
        }


class SetPasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    avatar = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "avatar",
            "password",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if request and not request.user.is_anonymous:
            return obj.subscribing.filter(user=request.user).exists()
        return False


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        if "password" not in data:
            raise serializers.ValidationError(
                {"password": "This field is required."}
            )
        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserSimpleSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    avatar = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "avatar",
        )

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if request and not request.user.is_anonymous:
            return obj.subscribing.filter(user=request.user).exists()
        return False


class SubscriptionSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source="author.email")
    id = serializers.ReadOnlyField(source="author.id")
    username = serializers.ReadOnlyField(source="author.username")
    first_name = serializers.ReadOnlyField(source="author.first_name")
    last_name = serializers.ReadOnlyField(source="author.last_name")
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    avatar = Base64ImageField(
        source="author.avatar", read_only=True, required=False
    )

    class Meta:
        model = Subscription
        fields = [
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
            "avatar",
        ]

    def get_is_subscribed(self, obj):
        user = (
            self.context.get("request").user
            if self.context.get("request")
            else None
        )
        if not user or user.is_anonymous:
            return False
        return obj.author.subscribing.filter(user=user).exists()

    def get_recipes(self, obj):
        request = self.context.get("request")
        try:
            limit = int(request.query_params.get("recipes_limit", 3))
        except (TypeError, ValueError):
            limit = 3

        recipes = obj.author.recipes.all()[:limit]
        return RecipeShortSerializer(
            recipes, many=True, context=self.context
        ).data

    def get_recipes_count(self, obj):
        return obj.author.recipes.count()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


class IngredientWriteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField(
        min_value=MIN_AMOUNT,
        max_value=MAX_AMOUNT,
        error_messages={
            "min_value": f"Количество должно быть не менее {MIN_AMOUNT}.",
            "max_value": f"Количество не должно превышать {MAX_AMOUNT}.",
        },
    )


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit"
    )

    class Meta:
        model = RecipeIngredient
        fields = ("id", "name", "measurement_unit", "amount")


class RecipeShortSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")


class RecipeReadSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(
        many=True, source="recipe_ingredients"
    )
    image = Base64ImageField(allow_null=False, required=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def get_is_favorited(self, obj):
        user = self.context["request"].user
        if user.is_anonymous:
            return False
        return obj.favorites.filter(user=user).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context["request"].user
        if user.is_anonymous:
            return False
        return obj.shopping_cart.filter(user=user).exists()


class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = IngredientWriteSerializer(many=True)
    image = Base64ImageField(allow_null=False, required=True)
    cooking_time = serializers.IntegerField(
        min_value=MIN_AMOUNT,
        max_value=MAX_AMOUNT,
        error_messages={
            "min_value": f"Время приготовления должно быть не менее {MIN_AMOUNT} минуты.",
            "max_value": f"Время приготовления не должно превышать {MAX_AMOUNT} минут.",
        },
    )
    name = serializers.CharField(max_length=MAX_NAME_LENGTH)
    text = serializers.CharField(min_length=MIN_TEXT_LENGTH)

    class Meta:
        model = Recipe
        fields = (
            "ingredients",
            "image",
            "name",
            "text",
            "cooking_time",
        )

    def validate(self, data):
        try:
            image = data.get("image")
            if image is None or image == "":
                raise serializers.ValidationError(
                    {"image": "Это поле обязательно."}
                )

            ingredients = data.get("ingredients")
            if not ingredients:
                raise serializers.ValidationError(
                    {"ingredients": "Нужен хотя бы один ингредиент"}
                )
            ingredient_ids = [item["id"] for item in ingredients]
            if len(ingredient_ids) != len(set(ingredient_ids)):
                raise serializers.ValidationError(
                    {"ingredients": "Ингредиенты не должны повторяться"}
                )

            # Validate ingredient amounts (redundant with IngredientWriteSerializer, but explicit)
            for ingredient in ingredients:
                amount = ingredient.get("amount")
                if not isinstance(amount, (int, float)) or amount <= 0:
                    raise serializers.ValidationError(
                        {
                            "ingredients": "Количество для ингредиента с id"
                            + f" {ingredient['id']} должно быть положительным числом."
                        }
                    )
        except Exception as e:
            raise serializers.ValidationError(
                {"validation": f"Ошибка валидации: {str(e)}"}
            )
        return data

    def _create_recipe_ingredients(self, recipe, ingredients_data):
        try:
            ingredient_ids = [item["id"] for item in ingredients_data]
            ingredients = Ingredient.objects.filter(id__in=ingredient_ids)
            ingredient_map = {
                ingredient.id: ingredient for ingredient in ingredients
            }
            missing_ids = set(ingredient_ids) - set(ingredient_map.keys())
            if missing_ids:
                raise serializers.ValidationError(
                    {
                        "ingredients": f"Ингредиенты с id "
                        + f"{', '.join(map(str, missing_ids))} не существуют."
                    }
                )
            recipe_ingredients = [
                RecipeIngredient(
                    recipe=recipe,
                    ingredient=ingredient_map[ingredient_data["id"]],
                    amount=ingredient_data["amount"],
                )
                for ingredient_data in ingredients_data
            ]
            RecipeIngredient.objects.bulk_create(recipe_ingredients)
        except Exception as e:
            raise serializers.ValidationError(
                {"ingredients": f"Ошибка при создании ингредиентов: {str(e)}"}
            )

    def create(self, validated_data):
        ingredients_data = validated_data.pop("ingredients")
        recipe = Recipe.objects.create(**validated_data)
        self._create_recipe_ingredients(recipe, ingredients_data)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop("ingredients")

        instance = super().update(instance, validated_data)
        instance.recipe_ingredients.all().delete()
        self._create_recipe_ingredients(instance, ingredients_data)
        return instance

    def to_representation(self, instance):
        return RecipeReadSerializer(instance, context=self.context).data


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), default=serializers.CurrentUserDefault()
    )
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())

    class Meta:
        model = Favorite
        fields = ("user", "recipe")
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=["user", "recipe"],
                message="Рецепт уже в избранном",
            )
        ]

    def validate(self, data):
        user = data.get("user")
        recipe = data.get("recipe")

        if recipe.favorites.filter(user=user).exists():
            raise serializers.ValidationError(
                {"errors": "Рецепт уже в избранном"}
            )
        return data

    def create(self, validated_data):
        return Favorite.objects.create(**validated_data)

    def to_representation(self, instance):
        return RecipeShortSerializer(
            instance.recipe, context=self.context
        ).data


class ShoppingCartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), default=serializers.CurrentUserDefault()
    )
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())

    class Meta:
        model = ShoppingCart
        fields = ("user", "recipe")
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=["user", "recipe"],
                message="Рецепт уже в списке покупок",
            )
        ]

    def validate(self, data):
        user = data.get("user")
        recipe = data.get("recipe")

        if recipe.shopping_cart.filter(user=user).exists():
            raise serializers.ValidationError(
                {"errors": "Рецепт уже в списке покупок"}
            )
        return data

    def create(self, validated_data):
        return ShoppingCart.objects.create(**validated_data)

    def to_representation(self, instance):
        return RecipeShortSerializer(
            instance.recipe, context=self.context
        ).data
