from django.shortcuts import render
from django.core.files.storage import FileSystemStorage


def upload(request):
    context = {}
    if request.method == "POST":
        request_file = request.FILES['document'] if 'document' in request.FILES else None
        if request_file:
                fs = FileSystemStorage()
                name = fs.save(request_file.name, request_file)
                context['url'] = fs.url(name)
    return render(request, 'uploader.html',context)


def create_room(request):
     return render(request, "create_room.html")


def join_room(request):
     return render(request, "join_room.html")

def room(request):
     return render(request, "room.html")


