from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Recipe,
    Favorite,
    Ingredient,
    RecipeIngredient,
    ShoppingCart,
)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "favorite_count")
    search_fields = ("name", "author__username")
    list_filter = ("name", "author")
    empty_value_display = "-пусто-"

    def favorite_count(self, obj):
        return Favorite.objects.filter(recipe=obj).count()

    favorite_count.short_description = "В избранном"


admin.site.register(Recipe, RecipeAdmin)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "measurement_unit")
    search_fields = ("name",)
    list_filter = ("name",)
    empty_value_display = "-пусто-"


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ("recipe", "ingredient", "amount")
    empty_value_display = "-пусто-"


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe")
    empty_value_display = "-пусто-"
