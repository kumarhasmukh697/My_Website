from django.shortcuts import render
from django.http import HttpResponse
from .models import Project,ImageGallary
from django.core.mail import send_mail

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
    if request.method == 'POST':
        name = request.POST.get('name')
        from_email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        recipient_list = ['kumarhasmukh697@gmail.com']

        full_message = f"From: {name}\nEmail: {from_email}\n\n{message}"

        send_mail(subject=subject,message=full_message,from_email=from_email,recipient_list=recipient_list,fail_silently=False,)

        return HttpResponse('OK')
