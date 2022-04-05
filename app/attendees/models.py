import uuid

from django.db import models


class Attendee(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    alexa_id = models.TextField(null=True)
    date_joined = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    date_deleted = models.DateField(default=None, null=True, blank=True)

    def __str__(self):
        return f"{self.full_name} {self.email} ({self.uuid})"

    @property
    def groups_list(self):
        group_list = []
        term_objs = self.attendees.all()
        for obj in term_objs:
            group_list.append(f"{obj.group.name} {obj.group.provider}")

        return group_list

