from django.shortcuts import get_object_or_404
from django.shortcuts import render
from rest_framework import viewsets

from .messages.email import send_invite_accepted
from .models import Event
from .models import Group
from .models import Term
from .models.access import AccessRequest
from .forms import CreateGroupForm, UpdateGroupForm
from .forms import CreateEventForm
from .serializers import AccessRequestSerializer
from .serializers import EventSerializer
from .serializers import GroupSerializer
from .serializers import TermSerializer
from django.views.generic.edit import UpdateView


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    lookup_field = "slug"

    def get_queryset(self):
        queryset = Group.objects.all()
        category = self.request.query_params.get('category')
        if category is not None:
            queryset = queryset.filter(category=category)
        return queryset


class TermViewSet(viewsets.ModelViewSet):
    queryset = Term.objects.all()
    serializer_class = TermSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class AccessViewSet(viewsets.ModelViewSet):
    queryset = AccessRequest.objects.all()
    serializer_class = AccessRequestSerializer


def access_view(request, token, response_code):
    access_request = get_object_or_404(AccessRequest, token=token, inactive=False)
    term = access_request.term
    response = "Approved" if response_code == "1" else "Declined"
    context = {
        "access": access_request,
        "attendee": access_request.proposer.full_name,
        "term": access_request.term,
        "token": access_request.token,
        "response": response
    }
    if response_code == "1":
        send_invite_accepted(attendee=access_request.proposer, event=access_request.term.current_event)
        term.attendees.add(access_request.proposer)
        term.save()

    access_request.inactive = True
    access_request.save()
    return render(request, "index.html", context)


class GroupUpdateView(UpdateView):
    model = Group
    form = CreateGroupForm
    form_additions = UpdateGroupForm
    fields = ('name', 'provider', 'description', 'category', 'active', 'public_contact')
    template_name = "groups/update_form.html"

    def get_context_data(self, **kwargs):
        context = super(GroupUpdateView, self).get_context_data(**kwargs)
        context.update({"page": "Group", "additions": self.form_additions})
        return context


class EventUpdateView(UpdateView):
    model = Event
    form = CreateEventForm
    fields = ('start_time', 'end_time')
    template_name = "groups/update_form.html"

    def get_context_data(self, **kwargs):
        context = super(EventUpdateView, self).get_context_data(**kwargs)
        context.update({"page": "Event"})
        return context

    def form_valid(self, form):
        form.instance.admin = self.request.user
        return super().form_valid(form)
