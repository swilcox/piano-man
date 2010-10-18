from django.http import HttpResponseRedirect, Http404
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from models import Project
import os
from django.contrib.auth.decorators import login_required

@login_required
def project(request, projectslug):
    print projectslug
    p = get_object_or_404(Project,slug=projectslug)
    try:
        readme = p.repo.get_file_contents('README.rst')
        readme_markup = 'rst'
    except:
        readme = ''
        readme_markup = 'txt'

    return render_to_response('projects/project.html',{'project':p,'readme':readme,'readme_markup':readme_markup},context_instance=RequestContext(request))


@login_required
def project_list(request,*args,**kwargs):
    projects = Project.objects.all()
    return render_to_response('projects/project_list.html',{'projects':projects},context_instance=RequestContext(request))

@login_required
def recent_commits(request, projectslug):
    project = get_object_or_404(Project,slug=projectslug)
    repo = project.repo
    #repo = get_object_or_404(CodeRepository, slug=slug)
    commits = repo.get_recent_commits()
    return render_to_response([
        'django_vcs/%s/recent_commits.html' % repo.name,
        'django_vcs/recent_commits.html',
    ], {'repo': repo, 'commits': commits}, context_instance=RequestContext(request))

@login_required
def code_browser(request, projectslug, path, **kwargs):
    project = get_object_or_404(Project,slug=projectslug)
    repo = project.repo
    rev = request.GET.get('rev') or None
    context = {'repo': repo, 'path': path, 'project':project}
    file_contents = repo.get_file_contents(path, rev)
    if file_contents is None:
        folder_contents = repo.get_folder_contents(path, rev)
        if folder_contents is None:
            raise Http404
        context['files'], context['folders'] = folder_contents
        context['files'] = [(os.path.join(path, o), o) for o in context['files']]
        context['folders'] = [(os.path.join(path, o), o) for o in context['folders']]
        return render_to_response([
            'django_vcs/%s/folder_contents.html' % repo.name,
            'django_vcs/folder_contents.html',
        ], context, context_instance=RequestContext(request))
    context['file'] = file_contents
    return render_to_response([
        'django_vcs/%s/file_contents.html' % repo.name,
        'django_vcs/file_contents.html',
    ], context, context_instance=RequestContext(request))

@login_required
def commit_detail(request, projectslug, commit_id):
    project = get_object_or_404(Project, slug=projectslug)
    repo = project.repo
    commit = repo.get_commit(commit_id)
    if commit is None:
        raise Http404
    return render_to_response([
        'django_vcs/%s/commit_detail.html' % repo.name,
        'django_vcs/commit_detail.html',
    ], {'project':project, 'repo': repo, 'commit': commit}, context_instance=RequestContext(request))

