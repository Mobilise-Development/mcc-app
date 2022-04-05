from django.db import models


class BaseModel(models.Model):
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    date_deleted = models.DateField(default=None, blank=True, null=True)

    objects = models.Manager()

    class Meta:
        abstract = True
