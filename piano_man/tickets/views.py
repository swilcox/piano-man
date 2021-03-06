from datetime import datetime

from django.db.models import Count
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext

from django_vcs.models import CodeRepository

from projects.models import Project

from tickets.filters import filter_for_project
from tickets.forms import TicketForm, get_ticket_form, TicketAttachmentForm
from tickets.models import Ticket, TicketReport

def ticket_list(request, projectslug):
    project = get_object_or_404(Project, slug=projectslug)
    if request.method == "POST":
        if not request.POST.get('report_name'):
            return redirect(request.get_full_path())
        TicketReport.objects.create(
            name=request.POST['report_name'],
            query_string=request.GET.urlencode(),
            project=project
        )
        return redirect('ticket_reports', projectslug=project.slug)
    tickets = project.tickets.all()
    filter = filter_for_project(project)(request.GET or None, queryset=tickets)
    return render_to_response([
        'tickets/%s/ticket_list.html' % project.name,
        'tickets/ticket_list.html',
    ], {'project': project, 'filter': filter}, context_instance=RequestContext(request))

def new_ticket(request, projectslug):
    project = get_object_or_404(Project, slug=projectslug)
    TicketDetailForm = get_ticket_form(project)
    if request.method == "POST":
        form = TicketForm(request.POST)
        detail_form = TicketDetailForm(request.POST)
        if form.is_valid() and detail_form.is_valid():
            ticket = form.save(commit=False)
            ticket.project = project
            ticket.creator = request.user
            ticket.created_at = datetime.now()
            ticket.save()
            detail_form.save(ticket)
            return redirect(ticket)
    else:
        form = TicketForm()
        detail_form = TicketDetailForm()
    return render_to_response([
        'tickets/%s/new_ticket.html' % project.name,
        'tickets/new_ticket.html',
    ], {'project': project, 'form': form, 'detail_form': detail_form}, context_instance=RequestContext(request))

def ticket_detail(request, projectslug, ticket_id):
    project = get_object_or_404(Project, slug=projectslug)
    ticket = get_object_or_404(project.tickets.all(), pk=ticket_id)
    TicketDetailForm = get_ticket_form(project, edit=True)
    if request.method == "POST":
        detail_form = TicketDetailForm(request.POST)
        if detail_form.is_valid():
            detail_form.save(ticket, new=False, user=request.user)
            ticket.save()
            return redirect(ticket)
    else:
        detail_form = TicketDetailForm(initial=dict([
            (selection.option.name, selection.choice_id) for selection in ticket.selections.all()
        ] + [('closed', ticket.closed)]))
    return render_to_response([
        'tickets/%s/ticket_detail.html' % project.name,
        'tickets/ticket_detail.html',
    ], {'project': project, 'ticket': ticket, 'detail_form': detail_form}, context_instance=RequestContext(request))

def nums_for_option(option, qs=None):
    if qs is None:
        qs = option.choices.all()
    qs = qs.annotate(c=Count('ticketoptionselection')).values_list('text', 'c')
    data = sorted(qs, key=lambda o: o[1], reverse=True)
    total = sum([o[1] for o in data])
    return data, total

def ticket_reports(request, projectslug):
    project = get_object_or_404(Project, slug=projectslug)
    reports = project.reports.all()
    return render_to_response([
        'tickets/%s/ticket_reoprts.html' % project.name,
        'tickets/ticket_reports.html',
    ], {'project': project, 'reports': reports}, context_instance=RequestContext(request))

def ticket_attachment(request, projectslug, ticket_id, attachment_id):
    project = get_object_or_404(Project, slug=projectslug)
    ticket = get_object_or_404(project.tickets.all(), pk=ticket_id)
    attachment = get_object_or_404(ticket.attachments.all(), pk=attachment_id)
    return render_to_response([
        'tickets/%s/ticket_attachment.html' % project.name,
        'tickets/ticket_attachment.html',
    ], {'project': project, 'ticket': ticket, 'attachment': attachment}, context_instance=RequestContext(request))

def ticket_new_attachment(request, projectslug, ticket_id):
    project = get_object_or_404(Project, slug=projectslug)
    ticket = get_object_or_404(project.tickets.all(), pk=ticket_id)
    if request.method == "POST":
        form = TicketAttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            attachment = form.save(commit=False)
            attachment.ticket = ticket
            attachment.uploaded_by = request.user
            attachment.save()
            changes = ticket.changes.create(
                user=request.user,
                text=attachment.description,
                at=attachment.uploaded_at
            )
            changes.changes.create(option="Attachment", to_text=attachment.file_name())
            return redirect(attachment)
    else:
        form = TicketAttachmentForm()
    return render_to_response([
        'tickets/%s/new_attachment.html' % project.name,
        'tickets/new_attachment.html',
    ], {'project': project, 'ticket': ticket, 'form': form}, context_instance=RequestContext(request))

def ticket_option_charts(request, projectslug):
    project = get_object_or_404(Project, slug=projectslug)
    options = project.ticketoption_set.all()
    data = {}
    for option in options:
        data[option.name] = nums_for_option(option)
    return render_to_response([
        'tickets/%s/ticket_option_charts.html' % project.name,
        'tickets/ticket_option_charts.html'
    ], {'project': project, 'data': data}, context_instance=RequestContext(request))

def ticket_option_chart(request, projectslug, option):
    project = get_object_or_404(Project, slug=projectslug)
    option = get_object_or_404(project.ticketoption_set, name__iexact=option)
    filter_class = filter_for_project(project, exclude=[option.name])
    filter = filter_class(request.GET or None, queryset=project.tickets.all())
    data, total = nums_for_option(option,
        option.choices.filter(ticketoptionselection__ticket__in=filter.qs)
    )
    context = {
        'project': project,
        'option': option,
        'data': data,
        'total': total,
        'options': project.ticketoption_set.exclude(id=option.id),
        'filter': filter
    }
    return render_to_response([
        'tickets/%s/ticket_option_chart.html' % project.name,
        'tickets/ticket_option_chart.html',
    ], context, context_instance=RequestContext(request))
