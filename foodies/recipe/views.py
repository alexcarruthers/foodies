from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from foodies.recipe.models import Recipe
from foodies.recipe.forms import RecipeForm, IngredientFormSet
from django.template import RequestContext
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.models import User
from guardian.shortcuts import assign, get_objects_for_user


@login_required
def list_my_recipes(request):
    recipe_list = Recipe.objects.filter(user=request.user).order_by('-created')

    return render_to_response('recipe/listrecipes.html', {
        'recipe_list': recipe_list,
        'username': request.user.get_full_name()
    }, context_instance=RequestContext(request))


def list_user_recipes(request, pk):
    user = get_object_or_404(User, pk=pk)
    recipe_list = Recipe.objects.filter(user=user).filter(is_public=True).order_by('-created')

    return render_to_response('recipe/listrecipes.html', {
        'recipe_list': recipe_list,
        'username': user.get_full_name()
    }, context_instance=RequestContext(request))


def list_recipes(request):
    recipe_list = Recipe.objects.filter(is_public=True)
    if request.user.is_authenticated():
        recipe_list |= get_objects_for_user(request.user, 'recipe.view_recipe')

    recipe_list = recipe_list.order_by('-created')

    return render_to_response('recipe/listrecipes.html', {'recipe_list': set(recipe_list)},
                              context_instance=RequestContext(request))


def view_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.user.has_perm('recipe.view_recipe', recipe) or recipe.is_public:
        return render_to_response('recipe/view_recipe.html', {'recipe': recipe},
                                  context_instance=RequestContext(request))
    else:
        return HttpResponseForbidden()


@login_required
def create_update_recipe(request, recipe_id=None):
    recipe = None

    if recipe_id:
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if not request.user.has_perm("recipe.change_recipe", recipe):
            return HttpResponseForbidden()
    else:
        if not request.user.has_perm("recipe.add_recipe"):
            return HttpResponseForbidden()

    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        formset = IngredientFormSet(request.POST, instance=recipe)
        if form.is_valid() and formset.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            
            for form in formset:
                if form.has_changed():
                    ingredient = form.save(commit=False)
                    ingredient.recipe = recipe
                    ingredient.save()

            assign('recipe.view_recipe', request.user, recipe)
            assign('recipe.change_recipe', request.user, recipe)
            assign('recipe.delete_recipe', request.user, recipe)

            return redirect(reverse('view_recipe', args=[recipe.id]))
    else:
        form = RecipeForm(instance=recipe)
        formset_instance = recipe if recipe else Recipe()
        formset = IngredientFormSet(instance=formset_instance)

    return render_to_response('recipe/create_update_recipe.html', {
        'form': form,
        'formset': formset,
        'recipe': recipe
    }, context_instance=RequestContext(request))


@login_required
def delete_recipe(request, recipe_id):
    try:
         recipe = Recipe.objects.get(pk=recipe_id)
         recipe.delete()
    except Recipe.DoesNotExist:
        raise Http404
    recipe_list = Recipe.objects.filter(user=request.user).order_by('-created')
    return render_to_response('recipe/listrecipes.html', {'recipe_list': recipe_list,
                                                          'username': request.user.get_full_name()},
                              context_instance=RequestContext(request))


def search_recipes(request):
    final_list = []
    search_input = ''
    if 'searchInput' in request.GET:
        search_input = request.GET['searchInput']
        if search_input != None and search_input.strip() != '':
            recipe_list = Recipe.objects.order_by('-created')
            splitInput = search_input.split()
            sorting_list = []
            for recipe in recipe_list:
                searchedRecipe = searchObject(recipe, splitInput)
                if searchedRecipe.is_not_none():
                    sorting_list.append(searchedRecipe)
            
            sorted_list = sorted(sorting_list, key = lambda x: (x.nameCount, x.userCount, x.prepCount, x.ingredientsCount), reverse=True)
             
            for item in sorted_list:
                final_list.append(item.recipe)
        else:
            search_input = ''
            final_list = []
    else:
        final_list = [] 
    return render_to_response('recipe/search.html', {'recipe_list': 
        final_list, 'input_value':'+'.join(search_input.split())}, context_instance=RequestContext(request))

class searchObject():
    def __init__(self, recipe, splitInput):
        self.nameCount = 0
        self.userCount = 0
        self.prepCount = 0
        self.ingredientsCount = 0
        self.recipe = recipe
        self.calculateCount(splitInput)
    
    def is_not_none(self):
        total = self.nameCount + self.userCount + self.prepCount + self.ingredientsCount
        if total == 0:
            return False
        else:
            return True

    def calculateCount(self, splitInput):
        for i in splitInput:
            self.nameCount = self.recipe.name.lower().split().count(i.lower())
            self.userCount = self.recipe.user.get_full_name().lower().split().count(i.lower())
            self.prepCount = self.recipe.prep_steps.lower().split().count(i.lower())
            for ingredient in self.recipe.ingredients.all():
                self.ingredientsCount = ingredient.name.lower().split().count(i.lower())
