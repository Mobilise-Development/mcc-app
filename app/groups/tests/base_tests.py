from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import Client
from django.utils import timezone
from rest_framework.test import APITestCase

from attendees.models import Attendee
from groups.models import Event
from groups.models import Group
from groups.models import Term
from groups.models.access import AccessRequest


class BaseTestCase(APITestCase):
    def setUp(self):
        self.client = Client()

        self.user = get_user_model().objects.create_admin_user(
            email="test_user@test.com",
            password="this is a cool password"
        )
        self.attendee_one = Attendee.objects.create(
            full_name="test_person",
            email="test@test.com",
            alexa_id="1234"
        )
        self.attendee_two = Attendee.objects.create(
            full_name="test_person_2",
            email="test2@test.com",
            alexa_id="12345"
        )
        self.group = Group.objects.create(
            name="test group",
            description="this is a test",
            active=True,
            public_contact="This is where you contact",
            admin=self.user,
            slug="badger"
        )
        #
        self.term = Term.objects.create(
            group=self.group,
            join_url="https://www.google.com",
            location="the moon"
        )

        self.inactive_term = Term.objects.create(
            group=self.group,
            join_url="https://www.askjeeves.com",
            location="Jupiter"
        )

        self.term.attendees.set([self.attendee_one, self.attendee_two])

        self.event = Event.objects.create(
            start_time=timezone.now() + timedelta(days=5),
            end_time=timezone.now() + timedelta(days=5),
            term=self.term,
        )
        self.past_event = Event.objects.create(
            start_time=timezone.now() + timedelta(days=-5),
            end_time=timezone.now() + timedelta(days=-5),
            term=self.inactive_term,
        )
        self.access_request = AccessRequest.objects.create(
            proposer=self.attendee_two,
            term=self.term
        )
        self.access_request_inactive = AccessRequest.objects.create(
            proposer=self.attendee_two,
            term=self.term,
            inactive=True
        )

    def tearDown(self) -> None:
        Term.objects.all().delete()
        Group.objects.all().delete()
        Attendee.objects.all().delete()
        Event.objects.all().delete()
        get_user_model().objects.all().delete()
        AccessRequest.objects.all().delete()
