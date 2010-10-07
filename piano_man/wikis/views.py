import os
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from projects.models import Project
from django.http import HttpResponse
import mimetypes

VALID_WIKI_EXTENSIONS = ['.creole','.textile','.markdown','.rst','.html']

def wiki_page(request, projectslug, path, **kwargs):
    project = get_object_or_404(Project,slug=projectslug)
    wiki = project.wiki
    path_to_page = path
    if path_to_page == '' or path_to_page[-1] == '/':
        path_to_page += 'index'
    #extension stuff
    ext = os.path.splitext(path_to_page)[-1]
    if ext == '':
        path_to_page += '.creole'
        ext = '.creole'
    elif len(ext) and ext not in VALID_WIKI_EXTENSIONS:
        mimetype = mimetypes.guess_type(path_to_page)[0] or 'application/octet-stream'
        return HttpResponse(wiki.repo.get_file_contents(path_to_page),mimetype=mimetype)

    try:
        content = wiki.repo.get_file_contents(path_to_page)
        style = ext[1:]
    except:
        content = 'that wiki page *does not* exist'
        style = 'creole'

    return render_to_response('wikis/wiki_page.html', {'content':content,'style':style, 'project':project}, context_instance=RequestContext(request))



