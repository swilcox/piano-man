from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from models import Project


# Create your views here.
#need a view showing all projects
#  - links to all open issues
#  - links to all issues open/assigned to current user
#  - links to default/general wiki
#  - links to docs
#  - search over "everything"
#  - overview of stats
#  - dashboard

#need a project view...showing:
#  - short descrption
#  - number of open issues
#  - versions
#  - components
#  - links to: docs, wiki, open issues, all issues, new issue, project search...

def project(request, slug):
    print slug
    #p = Project.objects.filter(slug=slug)
    p = get_object_or_404(Project,slug=slug)
    return render_to_response('projects/project.html',{'project':p},context_instance=RequestContext(request))


def project_list(request,*args,**kwargs):
    projects = Project.objects.all()
    return render_to_response('projects/project_list.html',{'projects':projects},context_instance=RequestContext(request))

