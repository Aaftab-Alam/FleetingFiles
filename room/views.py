import os
import boto3
from botocore.client import Config
from django.shortcuts import render, HttpResponse, redirect
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse
from .forms import CreateRoom
from .models import Room, File
from django.conf import settings

def generate_presigned_url(object_name):
    s3_client = boto3.client('s3',region_name='ap-south-1',config=Config(signature_version='s3v4'), aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    response = s3_client.generate_presigned_url(
         'get_object', 
         Params={
              'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 
              'Key': object_name, 
              "ResponseContentType":'application/octet-stream',
              "ResponseContentDisposition": f'attachment; filename="{object_name}"',
              },
          ExpiresIn=10)
    return response


def upload(request):
     if request.method== "POST":
          request_file = request.FILES['document'] if 'document' in request.FILES else None
          room= Room.objects.get(rname=request.session['rname'])
          if request_file:
               file = File(
                    room= room,
                    file=request_file
               )
               #this will save the file to default storage configured in settings.py, we can later access the file name using object.name, and url using object.url.
               file.save()
               return redirect("room")
          return HttpResponse("No file found")
     return render(request, 'uploader.html')
          
def download_file(request, file_name):
     #validating if a user is logged in a room
     if 'rname' in request.session:
          requested_file=File.objects.get(file=file_name)

          #validating if the user requesting the file is from the same room where the file is available
          if (requested_file.room.rname ==  request.session['rname']):
               link=generate_presigned_url(file_name)
               return redirect(link)
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
          return render(request, "room.html", {'files':files,'rname':rname})
     else:
          return redirect('join_room')

