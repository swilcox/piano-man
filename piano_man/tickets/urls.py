from django.conf.urls.defaults import *

ticket_urls = patterns('tickets.views',
    url(r'^$', 'ticket_list', name='ticket_list'),
    url(r'^$', 'new_ticket', name='new_ticket'),
    url(r'^(?P<ticket_id>\d+)/$', 'ticket_detail', name='ticket_detail'),
    url(r'^charts/(?P<option>[\w-]+)/$', 'ticket_option_chart', name='ticket_option_chart')
)

urlpatterns = patterns('',
    (r'^(?P<slug>[\w-]+)/', include(ticket_urls)),
)
