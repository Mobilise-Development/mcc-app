# send an email using credentials from Simple Email Service
from importlib import import_module

from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.utils import timezone

from comms.models import Email


class EmailBodyRenderError(Exception):
    pass


app_label = settings.MY_CELERY_APP
app = import_module(app_label).app

logger = get_task_logger(__name__)

email_folder = 'email'


def not_already_sent(dispatch_ref: str, to: str) -> bool:
    if dispatch_ref:
        try:
            email = Email.objects.get(dispatch_reference=dispatch_ref, recipient=to)
            return False
        except Email.DoesNotExist:
            pass

    return True


@app.task(name="comms.task.send-email")
def deliver_email(mjml_template: str, to: str, from_email: str, subject: str, dispatch_ref="", **kwargs) -> None:
    if not_already_sent(dispatch_ref, to):
        # create email object
        email_obj = Email.objects.create(
            subject=subject,
            recipient=to,
            sender=from_email,
            context=kwargs,
            mjml_template=mjml_template,
            dispatch_reference=dispatch_ref if dispatch_ref else None,
        )

        try:
            content = get_template(f"{email_folder}/{mjml_template}.mjml").render(kwargs)
            # update email object with content
            email_obj.content = content
            email_obj.save()
        except Exception as e:
            # if fails at this point email object will have no content
            logger.error(f"Error rendering email template: {e}")
            raise EmailBodyRenderError(f"Error rendering email template: {e}")

        try:
            logger.info("Processing delivery of email to {} from {}".format(to, from_email))
            msg = EmailMultiAlternatives(subject, content, from_email, [to])
            msg.attach_alternative(content, "text/ html")

            msg.send()
            # update email object with sent time
            email_obj.sent = timezone.now()
            email_obj.save()

        except Exception as e:
            logger.warning(f'*** mail error {e}')
