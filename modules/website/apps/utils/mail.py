import re

from django.core.mail import EmailMultiAlternatives, get_connection
from django.template import loader, Context
from django.conf import settings
from django.utils.html import strip_tags

def br2nl(content):
    nobr = re.compile('\s*<br.*?>\s*', re.I)
    return nobr.sub("\n", content) 

def send_multipart_mail(
    template_name, 
    email_context, 
    subject, 
    recipient, 
    sender=None,
    connection=None,
    fail_silently=False
):
    if not sender:
        sender = settings.DEFAULT_FROM_EMAIL

    connection = connection or get_connection(fail_silently=fail_silently)
    context = Context(email_context)    

    html_part = loader.get_template(template_name).render(context)
    text_part = strip_tags(br2nl(html_part)) 

    message = EmailMultiAlternatives(subject, text_part, sender, [recipient])
    message.attach_alternative(html_part, "text/html")
    message.content_subtype = "html"

    return connection.send_messages([message])
