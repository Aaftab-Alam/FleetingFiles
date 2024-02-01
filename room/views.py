import os
from django.shortcuts import render, HttpResponse, redirect
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse
from .forms import CreateRoom, LoginRoom
from .models import Room, File
from django.conf import settings


def upload(request):
     if request.method== "POST":
          request_file = request.FILES['document'] if 'document' in request.FILES else None
          room= Room.objects.get(rname=request.session['rname'])
          if request_file:
               fs= FileSystemStorage()
               name= fs.save(request_file.name, request_file)
               file_info = File(
                    room= room,
                    name=name,
                    file=fs.url(name)
               )
               file_info.save()
               return redirect("room")
          return HttpResponse("No file found")
     return render(request, 'uploader.html')
          
def download_file(request, file_name):
     if 'rname' in request.session:
          requested_file=File.objects.get(name=file_name)
          if (requested_file.room.rname ==  request.session['rname']):
               file_path = os.path.join(settings.MEDIA_ROOT, file_name)  # this will route the path "./room/media/file" to "./media/file"
               file = open(file_path, 'rb')
               response = FileResponse(file)
               response['Content-Type'] = 'application/octet-stream'
               response['Content-Disposition'] = f'attachment; filename="{file_name}"'
               return response
          else:
               return HttpResponse("File not found")
     return redirect('join_room')


def create_room(request):
     exists='false'
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
             room=Room.objects.get(rname=request.POST.get('rname'))
             if room:
                  exists='Room with that name already exists !'
             else:
                  exists='Room creation failed'     
     return render(request, "create_room.html",{'exists':exists})


def join_room(request):
     not_found='false'
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
             not_found='Invalid room name or password !'
        
     return render(request, "join_room.html",{'not_found':not_found})


def leave_room(request):
     request.session.flush()
     return redirect('/')

def room(request):
     if 'rname' in request.session:
          rname = request.session['rname']
          room = Room.objects.get(rname=rname)
          files = File.objects.filter(room=room)
          rname= request.session['rname']
          print(files)
          return render(request, "room.html", {'files':files,'rname':rname})
     else:
          return redirect('join_room')
     

          
     


