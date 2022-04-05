from rest_framework import serializers

from groups.models import Event
from groups.models import Group
from groups.models import Term
from groups.models.access import AccessRequest


class GroupSerializer(serializers.ModelSerializer):
    current_term = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = (
            'name', 'provider', 'description', 'category', 'admin', 'active', 'public_contact', 'slug', 'current_term', 'list_events'
        )
        lookup_field = "slug"

    def get_current_term(self, obj):
        current_term = obj.current_term
        return current_term.id if current_term else None


class TermSerializer(serializers.ModelSerializer):
    group = GroupSerializer

    class Meta:
        model = Term
        fields = ('group', 'attendees', 'attendees_count', 'join_url', 'term_active', 'next_event')


class EventSerializer(serializers.ModelSerializer):
    term = TermSerializer

    class Meta:
        model = Event
        fields = '__all__'


class AccessRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessRequest
        fields = '__all__'
