from datetime import datetime, timedelta
from itertools import chain
from operator import attrgetter

from django.db.models import Max, Q
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

#from django_vcs.models import CodeRepository
from projects.models import Project
from tickets.models import Ticket, TicketChange
from pyvcs.commit import Commit

from timeline.utils import normalize_attr

def timeline(request, projectslug):
    project = get_object_or_404(Project, slug=projectslug)
    since = datetime.now() - timedelta(days=5)
    items = list(chain(
        Ticket.objects.filter(project=project, created_at__gte=since).order_by('-created_at'),
        TicketChange.objects.filter(ticket__project=project, at__gte=since).order_by('-at'),
        project.repo.get_recent_commits(since),
    ))
    normalize_attr(items, 'canonical_date',
        keys={Ticket: 'created_at', Commit: 'time', TicketChange: 'at'})
    items = sorted(items, key=attrgetter('canonical_date'), reverse=True)
    return render_to_response([
        'timeline/%s/timeline.html' % project.name,
        'timeline/timeline.html',
    ], {'project': project, 'items': items}, context_instance=RequestContext(request))
