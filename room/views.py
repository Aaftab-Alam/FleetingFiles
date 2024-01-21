from django.shortcuts import render, HttpResponse

from django.core.files.storage import FileSystemStorage

from .forms import CreateRoom, LoginRoom
from .models import Room


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
     if request.method == 'POST':
        print(request.session.is_empty())
        form = CreateRoom(request.POST)
        if form.is_valid():
            room = Room(
                rname=form.cleaned_data['rname'],
                rpass=form.cleaned_data['rpass']
            )
            room.save()
            request.session['rname']=str(room.rname)
            print("Room Created")
            return HttpResponse("<h1>Room Created</h1>")
        else:
             return HttpResponse("Room Creation failed")
     return render(request, "create_room.html")


def join_room(request):
     return render(request, "join_room.html")

def room(request):
     return render(request, "room.html")


