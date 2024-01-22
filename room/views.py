from django.shortcuts import render, HttpResponse, redirect
from django.core.files.storage import FileSystemStorage
from .forms import CreateRoom, LoginRoom
from .models import Room, File


def upload(request):
    context = {}
    if request.method == "POST":
        request_file = request.FILES['document'] if 'document' in request.FILES else None
        if request_file:
                fs = FileSystemStorage()
                name = fs.save(request_file.name, request_file)
                # print(name, fs.url(name), fs.path(name))
                context['url'] = fs.url(name)
    return render(request, 'uploader.html',context)

def upload2(request):
     context={}
     if request.method== "POST":
          request_file = request.FILES['document'] if 'document' in request.FILES else None
          room= Room.objects.get(rname=request.session['rname'])
          if request_file:
               fs= FileSystemStorage()
               name= fs.save(request_file.name, request_file)

               file_info = File(
                    room= room,
                    file=fs.url(name)
               )
               file_info.save()
               return HttpResponse("File uploaded successfully")
          return HttpResponse("No file found")
     return render(request, 'uploader.html',context)
          



def create_room(request):
     if request.method == 'POST':
        request.session.flush()
        form = CreateRoom(request.POST)
        if form.is_valid():
            room=Room (
                 rname= form.cleaned_data['rname'],
                 rpass= form.cleaned_data['rpass']
            )
            room.save()
            request.session['rname']=str(room.rname)
            return redirect('room')
        else:
             return HttpResponse("Room Creation failed")
     return render(request, "create_room.html")


def join_room(request):
     if 'rname' in request.session:
          return redirect('room')
     if request.method == 'POST':
        rname= request.POST.get('rname')
        rpass= request.POST.get('rpass')
        try:
             room = Room.objects.get(rname=rname, rpass=rpass)
             print(room)
             request.session['rname']=str(room.rname)
             return redirect('room')
        
        except Room.DoesNotExist as e:
             return HttpResponse("Room not found")
        
     return render(request, "join_room.html")


def leave_room(request):
     request.session.flush()
     return redirect('/')

def room(request):
     if 'rname' in request.session:
          return render(request, "room.html")
     else:
          return redirect('join_room')
     

          
     


