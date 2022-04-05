from importlib import import_module

from django.conf import settings
from django.utils import timezone

from groups.messages.email import send_event_reminder
from groups.models import Event

app_label = settings.MY_CELERY_APP
app = import_module(app_label).app


@app.task(name='groups.tasks.reminder')
def send_event_reminders():
    events = Event.objects.filter(
        term__attendees__isnull=False,
        start_time__gte=timezone.now() - timezone.timedelta(minutes=15),
        start_time__lte=timezone.now() + timezone.timedelta(minutes=15),
        date_deleted__isnull=True
    ).distinct()

    for event in events:
        attendees = event.term.attendees.all()
        for attendee in attendees:
            send_event_reminder(attendee, event)
