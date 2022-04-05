from django.urls import reverse
from rest_framework import status

from groups.tests.base_tests import BaseTestCase


class EventViewSetTestCase(BaseTestCase):

    def test_event_list_view(self):
        response = self.client.get(reverse("events-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_retrieve_view(self):
        response = self.client.get(reverse("events-detail", kwargs={"pk": self.event.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
