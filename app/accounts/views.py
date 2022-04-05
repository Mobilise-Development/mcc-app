from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from groups.forms import CreateEventForm
from groups.forms import CreateGroupForm
from groups.models import Group, Term, Event


# Create your views here.
@login_required
def home(request):
    users_groups = Group.objects.filter(admin=request.user)
    events = Event.objects.all()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        event_form = CreateEventForm(request.POST)
        if form.is_valid():
            form.instance.admin = request.user
            form.save()
            return HttpResponseRedirect('/')
        if event_form.is_valid():
            event_form.save()
            return HttpResponseRedirect('/')
    else:
        form = CreateGroupForm()
        event_form = CreateEventForm()

    context = {
        "user": request.user,
        "groups": users_groups,
        "events": events,
        "form": form,
        "event_form": event_form,
        "platform_name": settings.PLATFORM_NAME
    }
    return render(request=request, template_name='home.html', context=context)

