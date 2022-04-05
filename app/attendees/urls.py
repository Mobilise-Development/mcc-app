from django.urls import include, path
from rest_framework import routers

from attendees.views import AttendeeViewSet

router = routers.DefaultRouter()
router.register('', AttendeeViewSet, "attendee")

urlpatterns = [
    path('attendee/', include(router.urls))
]
