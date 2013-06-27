from django.contrib import admin
from foodies.recipe.models import Ingredient, Recipe

admin.site.register(Ingredient)
admin.site.register(Recipe)
