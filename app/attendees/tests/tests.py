from django.test import Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from attendees.models import Attendee


class AttendeeViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = Client()
        self.attendee = Attendee.objects.create(
            full_name="test_person",
            email="test@test.com",
            alexa_id="1234"
        )

    def test_attendee_list_view(self):
        response = self.client.get(reverse("attendee-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_attendee_retrieve(self):
        response = self.client.get(reverse("attendee-detail", kwargs={"uuid": self.attendee.uuid}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_attendee_post(self):
        response = self.client.post('/api/attendee/', {
            'full_name': 'Jeff Test',
            "email": "test@testing.com",
            "alexa_id": "rbf93u2yb239bf03yfbehoiwbf",
        }, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
