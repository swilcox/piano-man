from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin

from tickets.urls import ticket_urls

admin.autodiscover()

project_urls = patterns('',
    url(r'^timeline/$', 'timeline.views.timeline', name='timeline'),
    url(r'^tickets/', include(ticket_urls)),
    url(r'^commit/(?P<commit_id>.*)/$', 'projects.views.commit_detail', name='commit_detail'),
    url(r'^browser/(?P<path>.*)$', 'projects.views.code_browser', name='code_browser'),
    url(r'^wiki/(?P<path>.*)$', 'wikis.views.wiki_page', name='wiki_page'),
    url(r'^$','projects.views.project',name='project'),
)

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^$','projects.views.project_list',name='project_list'),
    url(r'^(?P<projectslug>[\w-]+)/', include(project_urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
