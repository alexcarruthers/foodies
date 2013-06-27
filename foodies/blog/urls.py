from django.conf.urls import patterns, url

from views import *

urlpatterns = patterns('',
    url(r'^list/(?P<pk>\d+)/$', list_user_blogs, name='user_posts'),
    url(r'^me/$', list_my_posts, name="list_my_posts"),
    url(r'^add/$', create_update_post, name='create_post'),
    url(r'^(?P<pk>\d{1,12})/edit/$', create_update_post, name='update_post'),
    url(r'^(?P<pk>\d{1,12})/view/$', view_post, name='view_post'),
    url(r'^all/$', list_blogs, name='list_posts'),
    url(r'^(?P<pk>\d{1,12})/delete/$', delete_post, name='delete_post'),
    url(r'^search/$', search_blogs, name="search_blogs"),
)
