import uuid

from django.db import models
from django.urls import reverse

from attendees.models import Attendee
from groups.messages.email import send_attendee_join_request
from groups.models import Term
from groups.models.base import BaseModel


class AccessRequest(BaseModel):
    proposer = models.ForeignKey(Attendee, on_delete=models.CASCADE, related_name="access_proposer")
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name="access_term")
    token = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    inactive = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('access-request', kwargs={"token": self.token})

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        send_email = False
        if self.pk is None:
            send_email = True
        super().save(force_insert, force_update, using, update_fields)

        if self.inactive is False:
            send_attendee_join_request(
                attendee=self.proposer,
                event=self.term.current_event,
                access_request=self
            )
