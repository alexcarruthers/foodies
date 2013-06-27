from django.conf.urls import patterns, url
from views import *
from djangoratings.views import AddRatingFromModel

urlpatterns = patterns('',
    url(r'^all/$', list_recipes, name='list_recipes'),
    url(r'^list/(?P<pk>\d+)/$', list_user_recipes, name='user_recipes'),
    url(r'^me/$', list_my_recipes, name="list_my_recipes"),
    url(r'^create/$', create_update_recipe, name="create_recipe"),
    url(r'^(?P<recipe_id>\d+)/$', view_recipe, name="view_recipe"),
    url(r'^(?P<recipe_id>\d+)/update/$', create_update_recipe, name="update_recipe"),
    url(r'^(?P<recipe_id>\d+)/view/$', view_recipe),
    url(r'^(?P<recipe_id>\d+)/delete/$', delete_recipe, name="delete_recipe"),
    url(r'^(?P<object_id>\d+)/rate/(?P<score>\d+)/', AddRatingFromModel(), {
        'app_label': 'recipe',
        'model': 'recipe',
        'field_name': 'rating',
    }),
    url(r'^search/$', search_recipes, name="search_recipes")
)

