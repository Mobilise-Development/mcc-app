from django.test.client import encode_multipart
from django.urls import reverse
from rest_framework import status

from groups.tests.base_tests import BaseTestCase


class TermViewSetTestCase(BaseTestCase):

    def test_term_list_view(self):
        response = self.client.get(reverse("terms-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_term_retrieve_view(self):
        response = self.client.get(reverse("terms-detail", kwargs={"pk": self.term.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_term_active(self):
        self.assertEqual(self.term.term_active, True)

    # TODO: currently this is set to True, but it should be False as we don't need it as a feature right now
    # def test_term_inactive(self):
    #     self.assertEqual(self.inactive_term.term_active, False)

    def test_remove_attendee_from_term(self):
        attendee = str(self.attendee_one.uuid)
        group = self.term.group.pk
        join_url = self.term.join_url
        payload = {
            "group": group,
            "attendees": [attendee],
            "join_url": join_url
        }
        content = encode_multipart('BoUnDaRyStRiNg', payload)
        content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
        response = self.client.put(
            reverse("terms-detail", kwargs={"pk": self.term.pk}),
            data=content,
            content_type=content_type
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.attendee_one.uuid)
        self.assertNotContains(response, self.attendee_two.uuid)
