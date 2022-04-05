from __future__ import annotations

from django.conf import settings
from django.urls import reverse

from attendees.models import Attendee
from comms.tasks import deliver_email
from groups.models import Event


def send_invite_accepted(attendee, event: Event):
    context = dict(
        group=dict(
            name=event.term.group.name,
            provider=event.term.group.provider,
            email=event.term.group.public_contact,
            link=event.term.join_url,
        ),
        first_name=attendee.full_name,
        platform_name=settings.PLATFORM_NAME
    )

    send_attendee_email(
        attendee=attendee,
        mjml_template="invite_accepted",
        subject="Invite Accepted",
        **context
    )


def send_event_reminder(attendee, event, interval_id=15):
    context = dict(
        group=dict(
            name=event.term.group.name,
            provider=event.term.group.provider,
            email=event.term.group.public_contact,
            link=event.term.join_url,
        ),
        first_name=attendee.full_name,
        platform_name=settings.PLATFORM_NAME,
        start_time=event.start_time.strftime("%A, %d %B %Y %I:%M%p"),
    )
    send_attendee_email(
        attendee=attendee,
        mjml_template="event_reminder",
        subject="Event Reminder",
        dispatch_ref=f"{event.pk}-{attendee.pk}-{interval_id}-reminder",
        **context
    )


def send_attendee_join_request(attendee: Attendee, event: Event, access_request: "AccessRequest"):
    context = dict(
        attendee=dict(
            first_name=attendee.full_name,
            email=attendee.email, ),
        group=dict(
            name=event.term.group.name,
            provider=event.term.group.provider,
            link=event.term.join_url,
        ),
        invite=dict(
            decline=f"https://gwentgroups.mobilise.consulting{reverse('access-request', kwargs={'token': access_request.pk, 'response_code': 0})}",
            approve=f"https://gwentgroups.mobilise.consulting{reverse('access-request', kwargs={'token': access_request.pk, 'response_code': 1})}"
        )
    )
    send_system_to_admin_email(
        event=event,
        mjml_template="join_request",
        subject="Join Request",
        **context
    )


def send_attendee_email(attendee: Attendee, mjml_template: str, subject: str, dispatch_ref="", **kwargs):
    send_email(
        to=attendee.email,
        from_email=settings.EMAIL_DEFAULT_ADDRESS,
        mjml_template=mjml_template,
        subject=subject,
        dispatch_ref=dispatch_ref,
        **kwargs
    )


def send_system_to_admin_email(
        mjml_template: str,
        subject: str,
        event: Event,
        dispatch_ref="",
        **kwargs
):
    send_email(to=event.term.group.admin.email, from_email=settings.EMAIL_DEFAULT_ADDRESS,
               mjml_template=mjml_template,
               subject=subject, dispatch_ref=dispatch_ref, **kwargs)


def send_email(to: str, from_email: str, mjml_template: str, subject: str, dispatch_ref="", **kwargs):
    deliver_email.delay(
        mjml_template=mjml_template,
        to=to,
        from_email=from_email,
        subject=subject,
        dispatch_ref=dispatch_ref,
        **kwargs
    )
