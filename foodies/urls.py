from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import mainpage
import os

import gargoyle
gargoyle.autodiscover()

admin.autodiscover()

urlpatterns = patterns('',
    # Enable if you want feed streams to be exposed
    #('^activity/', include('actstream.urls')),
    (r'^announcements/', include('announcements.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^comments/', include('django.contrib.comments.urls')),

    (r'^account/', include('foodies.account.urls')),

    (r'^recipes/', include('foodies.recipe.urls')),

    (r'^post/', include('foodies.blog.urls')),

    url(r'^$', mainpage, name='mainpage'),
)

if 'PLATFORM' in os.environ and os.environ['PLATFORM'] == 'heroku':
    from conf.heroku_settings import STATIC_ROOT
    urlpatterns += patterns('', (r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': STATIC_ROOT}),)

