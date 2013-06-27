from foodies.recipe.models import Recipe, Ingredient
from django.forms import ModelForm
from django.forms.models import inlineformset_factory


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        exclude = ('user', 'ingredients')
        
         
class IngredientForm(ModelForm):
    class Meta:
        model = Ingredient

IngredientFormSet = inlineformset_factory(Recipe, Ingredient, extra=3)
