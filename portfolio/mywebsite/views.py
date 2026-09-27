import logging
import smtplib

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .models import Project, ImageGallary


logger = logging.getLogger(__name__)

# Create your views here.
def home(request):
    projects = Project.objects.all()
    return render(request, 'main.html', {'projects': projects})


def portfolio_details(request,id):
    project = Project.objects.get(id=id)
    images = ImageGallary.objects.filter(project=project)
    context = {'project': project,'images': images}
    return render(request, 'portfolio_details.html', context)



@require_POST
def send_message(request):
    name = (request.POST.get('name') or '').strip()
    from_email = (request.POST.get('email') or '').strip()
    subject = (request.POST.get('subject') or '').strip()
    message = (request.POST.get('message') or '').strip()
    contact_url = f"{reverse('home')}#contact"

    if not all((name, from_email, subject, message)):
        messages.error(request, 'Please complete all fields before sending your message.')
        return redirect(contact_url)

    try:
        validate_email(from_email)
    except ValidationError:
        messages.error(request, 'Please enter a valid email address.')
        return redirect(contact_url)

    if '\r' in subject or '\n' in subject:
        messages.error(request, 'Please enter a valid subject.')
        return redirect(contact_url)

    if not settings.EMAIL_HOST or not settings.DEFAULT_FROM_EMAIL:
        logger.error('Contact email could not be sent: SMTP host or sender is not configured.')
        messages.error(request, 'Email sending is not configured right now. Please try again later.')
        return redirect(contact_url)

    full_message = f"From: {name}\nEmail: {from_email}\n\n{message}"
    email = EmailMessage(
        subject=subject,
        body=full_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=['kumarhasmukh697@gmail.com'],
        reply_to=[from_email],
    )

    try:
        sent_count = email.send(fail_silently=False)
    except (OSError, smtplib.SMTPException):
        logger.exception('Failed to send contact email.')
        messages.error(request, 'Your message could not be sent. Please try again later.')
        return redirect(contact_url)

    if sent_count != 1:
        logger.error('Contact email backend did not send the message.')
        messages.error(request, 'Your message could not be sent. Please try again later.')
        return redirect(contact_url)

    messages.success(request, 'Your message has been sent. Thank you!')
    return redirect(contact_url)
