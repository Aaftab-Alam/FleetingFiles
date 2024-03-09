from datetime import datetime, timedelta
from functools import wraps

import boto3
import pytz
from botocore.client import Config
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import HttpResponse, redirect, render

from FleetingFiles.celery import app

from .forms import CreateRoom
from .models import File, Room

"""
Views for managing rooms and files.

Functions:
- get_s3_client: Get an S3 client.
- room_required: Decorator to require a room for a view function.
- create_room: Create a new room.
- join_room: Join an existing room.
- leave_room: Leave the current room.
- room: View the current room.
- delete_s3_objects: Delete AWS S3 objects.
- delete_room: Delete the current room.
- upload: Upload a file to the current room.
- generate_presigned_url: Generate a presigned URL for a file.
- download_file: Download a file from the current room.

"""


def get_s3_client():
    """
    Get an S3 client to perform CRUD and more operations.

    Returns:
        botocore.client.S3: The S3 client instance.

    Examples:
        >>> get_s3_client()
        <botocore.client.S3>
    """

    return boto3.client(
        "s3",
        region_name="ap-south-1",
        config=Config(signature_version="s3v4"),
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )


def room_required(view_func):
    """
    This decorator could be used with functions where room is required in users sessions to call that function.
    If there is no room in user's session then this session asks them to join a room.

    Args:
        view_func (function): The view function to be decorated.

    Returns:
        function: The decorated view function.

    Examples:
        >>> @room_required
        ... def room(request):
        ...     pass
        ...
        >>> room_required(room)
        <function room at 0x...>
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if "rname" not in request.session:
            return redirect("join_room")
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def create_room(request):
    """
    Create a room.

    Args:
        request: The HTTP request object.

    Returns:
        If the request method is not POST, renders the "create_room.html" template.
        If request methos is POST and the form is valid, a new room is created,
        celery worker is called for automatically deleting the room after 30 minutes,
        redirects to the "room" view.
        Otherwise, renders the "create_room.html" template.

    Raises:
        None.
    """

    if request.method != "POST":
        return render(request, "create_room.html")

    # request.session.flush()
    form = CreateRoom(request.POST)
    if form.is_valid():
        room, created = Room.objects.get_or_create(
            rname=form.cleaned_data["rname"],
            defaults={"rpass": form.cleaned_data["rpass"]},
        )
        if created:
            request.session["rname"] = room.rname
            delete_room.apply_async(
                args=[room.rname],
                eta=datetime.now(pytz.timezone("UTC")) + timedelta(minutes=30),
            )
            return redirect("room")

    if form.has_error("rname", "unique"):
        messages.error(request, "Room with that name already exists!")
    else:
        messages.error(request, "Room creation failed")
    return render(request, "create_room.html")


def join_room(request):
    """
    Join a room using valid credentials.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects to the 'room' view if the room name and password are valid.

    Examples:
        >>> join_room(request)
        <HttpResponseRedirect>
    """

    if "rname" in request.session:
        return redirect("room")
    if request.method == "POST":
        rname = request.POST.get("rname")
        rpass = request.POST.get("rpass")
        if room := Room.objects.filter(rname=rname, rpass=rpass).first():
            request.session["rname"] = room.rname
            return redirect("room")
        else:
            messages.error(request, "Invalid room name or password!")
    return render(request, "join_room.html")


def leave_room(request):
    request.session.flush()
    return redirect("/")


@room_required
def room(request):
    """
    Render the room view. If room is not found in the database, it means room has already been expired.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered HTML template with all the files belonging to this room.

    Examples:
        >>> room(request)
        <HttpResponse>
    """
    rname = request.session["rname"]
    try:
        room = Room.objects.get(rname=rname)
    except ObjectDoesNotExist:
        request.session.flush()
        return HttpResponse('<h3 align="center" style="font-family:Open Sans">Room has expired!</h3>')
    files = File.objects.filter(room=room)
    return render(request, "room.html", {"files": files, "rname": rname})


def delete_s3_objects(files):
    """
    Delete S3 objects(files belonging to a particular room).

    Args:
          files (QuerySet): The files to be deleted.

    Returns:
          bool: True if there are no files in a room. True if there are files in room and the deletion is successful, False otherwise.
    """
    if len(files) == 0:
        return True
    s3 = get_s3_client()
    s3.delete_objects(
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Delete={
            "Objects": [{"Key": file_obj.file.name} for file_obj in files],
            "Quiet": False,
        },
    )
    return True


@app.task
def delete_room(room_name):
    """
    Delete the current room with all the files belonging to it.

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        Union[HttpResponse, HttpResponseRedirect]: The HTTP response.

    """
    room = Room.objects.get(rname=room_name)
    files = File.objects.filter(room=room)
    if delete_s3_objects(files):
        files.delete()
        room.delete()
        return "Files deleted succesfully"
    else:
        return "Files deletion failed"


@room_required
def upload(request):
    """
    Upload a file to the current room.

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        Union[HttpResponse, HttpResponseRedirect]: The HTTP response.

    """
    if request.method != "POST":
        return render(request, "uploader.html")

    request_file = request.FILES.get("document")
    if not request_file:
        return HttpResponse("No file found")
    if request_file.size > 5242880 :  # File must not be greater than 5MB
        return HttpResponse('<h3 align="center" style="font-family:Open Sans">File size exceeds the limit of 5MB.</h3>')

    room = Room.objects.get(rname=request.session["rname"])
    file = File(room=room, file=request_file)
    # this will save the file to default storage configured in settings.py, we can later access the file name using object.name, and url using object.url.
    file.save()
    return redirect("room")


def generate_presigned_url(object_name):
    """
    Generate a presigned URL for a file to download. This URL will automatically expire after 10 seconds making it no longer usable.

    Args:
        object_name (str): The name of the file.

    Returns:
        str: The presigned URL.

    """
    s3_client = get_s3_client()
    return s3_client.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
            "Key": object_name,
            "ResponseContentType": "application/octet-stream",
            "ResponseContentDisposition": f'attachment; filename="{object_name}"',
        },
        ExpiresIn=10,
    )


@room_required
def download_file(request, file_name):
    """
    Download a file from the current room.

    Args:
        request (HttpRequest): The HTTP request.
        file_name (str): The name of the file to download.

    Returns:
        Union[HttpResponse, HttpResponseRedirect]: The HTTP response.

    """
    try:
        requested_file = File.objects.get(file=file_name)
    except ObjectDoesNotExist:
        request.session.flush()
        return HttpResponse('<h3 align="center" style="font-family:Open Sans">Room has been expired<h3>')

    # validating if the user requesting the file is from the same room where the file is available
    if requested_file.room.rname == request.session["rname"]:
        link = generate_presigned_url(file_name)
        return redirect(link)
    return HttpResponse("File not found")
