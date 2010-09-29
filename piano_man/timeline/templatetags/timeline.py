from django import template
from django.template.loader import render_to_string

register = template.Library()

@register.simple_tag
def timeline_item(item, project, media_url):
    return render_to_string(
        'timeline/%s_obj.html' % type(item).__name__.lower(),
        {'item': item, 'project': project, 'MEDIA_URL': media_url}
    )
