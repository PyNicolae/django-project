from django.shortcuts import render,redirect
from django.http import FileResponse, HttpRequest,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import UploadForm
import os
import mimetypes
import uuid
from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import render
from requests import Response
from .models import Upload
# Create your views here.


def register(request):

    if request.method == "POST":
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass1')

        myuser = User.objects.create_user(username,pass1,pass2)
        myuser.username = username
        myuser.pass1 = pass1
        myuser.pass2 = pass2

        myuser.save()

        messages.success(request, "Your account has been created.")

        return redirect('signin')

    return render(request, "filetransfer/register.html")


def home(request):
    return render(request, "filetransfer/index.html")


def signin(request):

    if request.method == "POST":
        username = request.POST.get("username")
        pass1 = request.POST.get('pass1')

        user = authenticate(username=username,password=pass1)

        if user is not None:
            login(request, user)
            username = user.username
            return render(request, "filetransfer/index.html", {"username":username})

        else:
            messages.error(request, "Bad Credentials!")
            return redirect("home")

    return render(request, "filetransfer/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("home")

@login_required(login_url='signin')
def upload_file(request):

    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            file_extension = os.path.splitext(file.name)[1]
            file_name = str(uuid.uuid4()) + file_extension
            

            file_path = os.path.join(settings.MEDIA_ROOT, 'media', file_name)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            upload_file = Upload.objects.create

            request.session['file_name'] = file_name

            return redirect("download/")
            
    else:
        form = UploadForm()
    return render(request, 'filetransfer/upload.html', {'form': form})


def aboutus(request):
    return render(request, 'filetransfer/aboutus.html')


def download_file(request,file_name):
    file_path = os.path.join(settings.MEDIA_ROOT,"media", file_name)

    if not os.path.exists(file_path):
        raise Http404
    
    with open(file_path, "rb") as file:
        file_contents = file.read()
    
    response = HttpResponse(file_contents, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    
    return response


def download_page(request):
    try:
        uploaded_file = Upload.objects.last()
        file_name = request.session.get('file_name')
        file_path=os.path.join(settings.MEDIA_ROOT,"media",file_name)
        download_url = request.build_absolute_uri(reverse('download', args=[file_name]))

    except Upload.DoesNotExist:
        download_url = None

    return render(request, 'filetransfer/download.html', {'download_url': download_url})
