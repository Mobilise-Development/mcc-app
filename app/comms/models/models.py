from django.db import models

from .base import BaseModel


class Email(BaseModel):
    """
    Email model
    """
    dispatch_reference = models.CharField(max_length=255, blank=True, null=True)
    sender = models.EmailField()
    recipient = models.EmailField()
    subject = models.CharField(max_length=150)
    content = models.TextField(null=True, blank=True)
    sent = models.DateTimeField(blank=True, null=True)
    mjml_template = models.CharField(null=True, blank=True, max_length=50)
    context = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.recipient} - {self.subject} - {self.sent}"

    class Meta:
        verbose_name = 'Email'
        verbose_name_plural = 'Emails'
        ordering = ['-date_created']


class SMS(BaseModel):
    sender = models.CharField(max_length=150)
    recipient = models.CharField(max_length=150)
    body = models.CharField(max_length=256)

    def __str__(self):
        return self.sender

    class Meta:
        verbose_name_plural = "SMS"
        ordering = ['-date_created']
