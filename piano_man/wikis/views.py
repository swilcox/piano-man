from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext

from django_vcs.models import CodeRepository

from projects.models import Project


def wiki_page(request, projectslug, path, **kwargs):
    project = get_object_or_404(Project,slug=projectslug)
    return render_to_response('wikis/wiki_page.html', {'wp':{}, 'project':project}, context_instance=RequestContext(request))



