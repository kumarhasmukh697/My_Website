from django.shortcuts import render
from .models import Project, ImageGallary
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse



# Create your views here.
def home(request):
    projects = Project.objects.all()
    return render(request, 'main.html', {'projects': projects})


def portfolio_details(request,id):
    project = Project.objects.get(id=id)
    images = ImageGallary.objects.filter(project=project)
    context = {'project': project,'images': images}
    return render(request, 'portfolio_details.html', context)






def send_message(request):

    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "message": "Invalid request method."
        }, status=405)

    name = request.POST.get("name")
    email = request.POST.get("email")
    subject = request.POST.get("subject")
    message = request.POST.get("message")

    if not name or not email or not subject or not message:
        return JsonResponse({
            "success": False,
            "message": "Please fill in all fields."
        }, status=400)

    try:
        send_mail(
            subject=subject,
            message=f"Hello,\n\nName: {name}\nEmail: {email}\n\nMessage:\n{message}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=False,
        )

        return JsonResponse({
            "success": True,
            "message": "Your message has been sent successfully!"
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": "Unable to send your message. Please try again."
        }, status=500)