from django.urls import reverse
from rest_framework import status

from groups.tests.base_tests import BaseTestCase


class GroupViewSetTestCase(BaseTestCase):

    def test_group_list_view(self):
        response = self.client.get(reverse("groups-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_group_retrieve_view(self):
        response = self.client.get(reverse("groups-detail", kwargs={"slug": self.group.slug}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
