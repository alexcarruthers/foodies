from django.test import TestCase, Client
from foodies.recipe.models import *
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

import views


class ListAllRecipesViewTest(TestCase):
    def setUp(self):
        c = Client()
        self.response = c.get(reverse('list_recipes'))

    def test_views(self):
        responses = self.response.context['recipe_list']
        i = 1

        for recipe_response in responses:
            recipe = Recipe.objects.get(pk=i)
            pk = recipe.pk
            i += 1
            self.assertEqual(recipe_response.pk, pk)


class ListMyRecipesViewTest(TestCase):
    def setUp(self):
        self.c = Client()
        test_user = User.objects.create(
        		username = 'test_user_1',
        		password='!',
						first_name='test',
						last_name='user'
        		)
        test_user.set_password('1234')
        test_user.save()
        self.user = test_user
        self.c.login(username='test_user_1', password='1234')

        self.recipe_list = []
        self.recipe_list.append(Recipe.objects.create(
            name="Recipe!",
            user= test_user,
            prep_steps="A B D \n C E F",
            time_to_prepare=5,
            cooking_time=5
        ))
        self.recipe_list.append(Recipe.objects.create(
            name="Another Recipe",
            user= test_user,
            prep_steps="B A D \n C E F",
            time_to_prepare=4,
            cooking_time=7
        ))
        self.recipe_list.append(Recipe.objects.create(
            name="And Another Recipe!",
            user= test_user,
            prep_steps="A B D \n 5 \n E F",
            time_to_prepare=5,
            cooking_time=5
        ))
        

    def test_views(self):
        responses = self.c.get(reverse('list_my_recipes'), follow = True)
        context_responses = responses.context['recipe_list']
        i = len(context_responses)-1
        for recipe_response in context_responses:
            recipe = self.recipe_list[i]
            pk = recipe.pk
            i -= 1
            self.assertEqual(recipe_response.pk, pk)


class ListModelTest(TestCase):
    def setUp(self):
        self.recipe = Recipe.objects.create(
            name="Recipe!",
            user=User.objects.create(username = 'testuser'),
            prep_steps="A B D \n C E F",
            time_to_prepare=5,
            cooking_time=5
        )

    def test_models(self):
        count = 0
        for i in range(0, 2):
            try:
                recipe_response = Recipe.objects.get(pk=self.recipe.pk + i)
                name = recipe_response.name
                user = recipe_response.user
                prep = recipe_response.prep_steps
                timePrep = recipe_response.time_to_prepare
                cookTime = recipe_response.cooking_time

                self.assertEqual(self.recipe.name, name)
                self.assertEqual(self.recipe.user, user)
                self.assertEqual(self.recipe.prep_steps, prep)
                self.assertEqual(self.recipe.time_to_prepare, timePrep)
                self.assertEqual(self.recipe.cooking_time, cookTime)
                count = 1
            except:
                self.assertEqual(count, 1)


class SearchViewTest(TestCase):
    def setUp(self):
        self.testUser = User.objects.create_user(
            username='test_username',
            email='test@test.com',
            password='test'
        )
        self.testUser.first_name = 'testFirst'
        self.testUser.last_name = 'testSecond'

        self.testFailureUser = User.objects.create_user(
            username='test_failure_name',
            email='test2@test.com',
            password='test2'
        )
        self.testFailureUser.first_name = 'testThird'
        self.testFailureUser.last_name = 'testFourth'

        self.testUser.save()
        self.testFailureUser.save()

        self.testRecipe = Recipe.objects.create(
            name='test_recipe',
            user=self.testUser,
            prep_steps='test_steps',
            time_to_prepare=1,
            cooking_time=2
        )

        self.testFailureRecipe = Recipe.objects.create(
            name='test_failure_recipe',
            user=self.testFailureUser,
            prep_steps='test_steps',
            time_to_prepare=1,
            cooking_time=2
        )

        self.testRecipe.save()
        self.testFailureRecipe.save()

        self.url = reverse('search_recipes')

    def test_search_recipe_view_renders(self):
        c = Client()
        response = c.get(self.url, data={'searchQuery': ''})

        # Test http response status, url, and html template
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipe/search.html')
        self.assertTemplateUsed(response, 'recipe/listrecipes.html')

    def test_search_recipe_view_by_recipe_name_success(self):
        c = Client()

        response = c.get(self.url, data={'searchInput': self.testRecipe.name})
        results = response.context['recipe_list']

        self.assertEquals(len(results), 1)
        for res in results:
            self.assertEquals(res.pk, self.testRecipe.pk)

    def test_search_recipe_view_by_user_success(self):
        c = Client()

        response = c.get(self.url, data={'searchInput': self.testRecipe.user.first_name})
        results = response.context['recipe_list']

        self.assertEquals(len(results), 1)
        for res in results:
            self.assertEquals(res.user.pk, self.testUser.pk)

        response = c.get(self.url, data={'searchInput': self.testRecipe.user.last_name})
        results = response.context['recipe_list']

        self.assertEquals(len(results), 1)
        for res in results:
            self.assertEquals(res.user.pk, self.testUser.pk)

    def test_search_recipe_view_by_name_failure(self):
        c = Client()

        response = c.get(self.url, data={'searchInput': self.testRecipe.name})
        results = response.context['recipe_list']

        for res in results:
            self.assertNotEquals(res.pk, self.testFailureRecipe.pk)

    def test_search_recipe_view_by_user_failure(self):
        c = Client()

        response = c.get(self.url, data={'searchInput': self.testRecipe.user.first_name})
        results = response.context['recipe_list']

        for res in results:
            self.assertNotEquals(res.user.pk, self.testFailureUser.pk)

        response = c.get(self.url, data={'searchInput': self.testRecipe.user.last_name})
        results = response.context['recipe_list']

        for res in results:
            self.assertNotEquals(res.user.pk, self.testFailureUser.pk)
