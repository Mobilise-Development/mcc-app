from django.contrib import admin

from groups.models import Event
from groups.models import Group
from groups.models import Term
from groups.models.access import AccessRequest

admin.site.register(Group)
admin.site.register(Term)
admin.site.register(Event)
admin.site.register(AccessRequest)
