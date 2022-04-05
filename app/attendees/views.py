from rest_framework import viewsets

from .models import Attendee
from .serializers import AttendeeSerializer


class AttendeeViewSet(viewsets.ModelViewSet):
    serializer_class = AttendeeSerializer
    lookup_field = "uuid"

    def get_queryset(self):
        queryset = Attendee.objects.all()
        email = self.request.query_params.get('email')
        if email is not None:
            queryset = queryset.filter(email=email)
        return queryset
