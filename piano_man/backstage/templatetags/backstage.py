import os

from django import template
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from django_vcs.models import CodeRepository
from projects.models import Project

register = template.Library()

class OtherProjects(template.Node):
    def __init__(self, project, varname):
        self.project = project
        self.varname = varname

    def render(self, context):
        project = self.project.resolve(context)
        if project:
            project = project.id
        else:
            project = None
        context[self.varname] = Project.objects.exclude(id=project)
        return ''

@register.tag
def get_other_projects(parser, token):
    bits = token.split_contents()
    bits.pop(0)
    project = parser.compile_filter(bits.pop(0))
    varname = bits.pop()
    return OtherProjects(project, varname)

@register.filter
def urlize_path(path, project):
    bits = path.split(os.path.sep)
    parts = []
    for i, bit in enumerate(bits[:-1]):
        parts.append('<a href="%(url)s">%(path)s</a>' % {
            'url': reverse('code_browser', kwargs={
                'path': '/'.join(bits[:i+1])+'/',
                'projectslug': project.slug,
            }),
            'path': bit,
        })
    return ' / '.join(parts + bits[-1:])

@register.inclusion_tag('backstage/nav_bar_urls.html')
def nav_bar_urls(project, nested):
    return {'project': project, 'nested': nested}

@register.inclusion_tag('backstage/chartlist.html', takes_context=True)
def chartlist(context, data, total, option):
    new_context = {
        'data': data,
        'total': total,
        'option': option,
        'request': context['request'],
        'project': context['project'],
    }
    return new_context

@register.inclusion_tag('backstage/form.html')
def render_form(form):
    return {'form': form}
