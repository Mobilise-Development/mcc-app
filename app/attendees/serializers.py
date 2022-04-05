from rest_framework import serializers

from attendees.models import Attendee


class AttendeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attendee
        lookup_field = 'uuid'
        fields = ('uuid', 'full_name', 'email', 'groups_list')
