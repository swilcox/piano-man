from django.conf.urls.defaults import *

urlpatterns = patterns('timeline.views',
    url(r'^(?P<projectslug>[\w-]+)/$', 'timeline', name='timeline'),
)
