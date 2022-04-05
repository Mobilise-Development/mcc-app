from django.urls import include
from django.urls import path
from rest_framework import routers

from groups import views
from groups.views import AccessViewSet
from groups.views import EventViewSet
from groups.views import GroupViewSet
from groups.views import TermViewSet
from groups.views import GroupUpdateView, EventUpdateView

router = routers.DefaultRouter()
router.register(r'groups/management', GroupViewSet, "groups")
router.register(r'groups/term', TermViewSet, "terms")
router.register(r'groups/event', EventViewSet, "events")
router.register(r'access', AccessViewSet, "access")

urlpatterns = [
    path('api/', include(router.urls)),
    path('access/<token>/<response_code>/', views.access_view, name="access-request"),
    path('group/<int:pk>/', GroupUpdateView.as_view(), name="group-update"),
    path('event/<int:pk>/', EventUpdateView.as_view(), name="event-update")
]
