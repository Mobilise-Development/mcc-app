from django.urls import reverse
from rest_framework import status

from groups.tests.base_tests import BaseTestCase


class AccessRequestAPITestCase(BaseTestCase):

    def test_access_list_view(self):
        response = self.client.get(reverse("access-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_access_retrieve_view(self):
        response = self.client.get(reverse("access-detail", kwargs={"pk": self.access_request.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_access_post(self):
        attendee = self.attendee_one.uuid
        term = self.term.pk
        data = {
            "proposer": attendee,
            "term": term
        }
        response = self.client.post(reverse("access-list"), data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class AccessRequestViewTests(BaseTestCase):

    def test_active_access_request(self):
        response_code = 0
        response = self.client.get(f"/access/{self.access_request.pk}/{response_code}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.access_request.inactive, False)

    def test_single_use_request(self):
        response_code = 1
        response = self.client.get(f"/access/{self.access_request.pk}/{response_code}/")
        response2 = self.client.get(f"/access/{self.access_request.pk}/{response_code}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)

    def test_inactive_access_request(self):
        response_code = 1
        response = self.client.get(f"/access/{self.access_request_inactive.pk}/{response_code}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
