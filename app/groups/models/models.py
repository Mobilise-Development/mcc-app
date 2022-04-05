from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone

from attendees.models import Attendee
from groups.models.base import BaseModel

READING = "READING"
CYCLING = "CYCLING"
CINEMA = "CINEMA"
GAMING = "GAMING"
TECH = "TECH"
CHESS = "CHESS"
CHATTING = "CHATTING"
EDUCATIONAL = "EDUCATIONAL"


class Group(BaseModel):
    CATEGORY_CHOICES = (
        (READING, "Reading"),
        (CYCLING, "Cycling"),
        (CINEMA, "Cinema"),
        (GAMING, "Gaming"),
        (TECH, "Tech"),
        (CHESS, "Chess"),
        (CHATTING, "Chatting"),
        (EDUCATIONAL, "Educational")
    )

    name = models.CharField(max_length=75)
    provider = models.CharField(max_length=75, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, null=True, blank=True)
    admin = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="admin", null=True)
    active = models.BooleanField(default=True)
    public_contact = models.EmailField(null=True, blank=True)
    slug = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("home")

    def save(self, *args, **kwargs):
        self.slug = f"{self.name}{self.provider}".lower().replace(" ", "")
        return super().save(*args, **kwargs)

    @property
    def current_term(self):
        terms = self.term.filter(group=self.id)
        for term_obj in terms:
            if term_obj.term_active:
                return term_obj

    @property
    def attendees_current_term(self):
        if self.current_term:
            return self.current_term.attendees.all()
        else:
            return []

    @property
    def list_events(self):
        current_term = self.current_term
        events = current_term.event.all()
        id_list = list()
        events_list = list()
        for event in events:
            id_list.append(event.id)
            events_list.append(
                {
                    "id": id_list,
                    "start_time": event.start_time,
                    "end_time": event.end_time
                }
            )
        return events_list

    class Meta:
        unique_together = ('name', 'provider',)
        ordering = ["-name"]


class Term(BaseModel):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="term")
    attendees = models.ManyToManyField(Attendee, related_name="attendees", blank=True)
    join_url = models.URLField()
    location = models.CharField(max_length=50)
    perpetual = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.group.name} {self.group.provider} {self.pk}"

    @property
    def administrator(self):
        return self.group.admin.email

    @property
    def attendees_count(self):
        if self.attendees:
            return self.attendees.all().count()
        return 0

    @property
    def term_active(self):
        if self.event.first():
            final_event = self.event.last()
            final_date = final_event.end_time
            if final_date > timezone.now():
                return True
        # return False if MCC go ahead with Terms.
        return True

    @property
    def next_event(self):
        event = self.event.filter(is_cancelled=False).first()

        return {
            "start_time": event.start_time,
            "end_time": event.end_time,
            "is_cancelled": event.is_cancelled
        }

    @property
    def current_event(self):
        event = self.event.filter(is_cancelled=False).first()
        return event


class Event(BaseModel):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name="event")
    is_cancelled = models.BooleanField(default=False)

    class Meta:
        ordering = ['-start_time']

    def get_absolute_url(self):
        return reverse("home")

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"
