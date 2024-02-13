from functools import wraps

import boto3
from botocore.client import Config
from django.conf import settings
from django.contrib import messages
from django.shortcuts import HttpResponse, redirect, render

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
    Decorator to require a room for a view function.

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
    if request.method != "POST":
        return render(request, "create_room.html")

    request.session.flush()
    form = CreateRoom(request.POST)
    if form.is_valid():
        room, created = Room.objects.get_or_create(
            rname=form.cleaned_data["rname"],
            defaults={"rpass": form.cleaned_data["rpass"]},
        )
        if created:
            request.session["rname"] = room.rname
            return redirect("room")

    if form.has_error("rname", "unique"):
        messages.error(request, "Room with that name already exists!")
    else:
        messages.error(request, "Room creation failed")
    return render(request, "create_room.html")


def join_room(request):
    """
    Join a room.

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
    Render the room view.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered HTML template with all the files belonging to this room.

    Examples:
        >>> room(request)
        <HttpResponse>
    """
    rname = request.session["rname"]
    room = Room.objects.get(rname=rname)
    files = File.objects.filter(room=room)
    return render(request, "room.html", {"files": files, "rname": rname})


def delete_s3_objects(files):
    """
    Delete S3 objects.

    Args:
          files (QuerySet): The files to be deleted.

    Returns:
          bool: True if the deletion is successful, False otherwise.
    """
    s3 = get_s3_client()
    s3.delete_objects(
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Delete={
            "Objects": [{"Key": file_obj.file.name} for file_obj in files],
            "Quiet": False,
        },
    )
    return True

@room_required
def delete_room(request):
    """
    Delete the current room with all the files belonging to it.

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        Union[HttpResponse, HttpResponseRedirect]: The HTTP response.

    """
    room = Room.objects.get(rname=request.session["rname"])
    files = File.objects.filter(room=room)
    if delete_s3_objects(files):
        files.delete()
        room.delete()
        request.session.flush()
        return redirect("/")
    else:
        return HttpResponse("Files deletion failed")


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
    requested_file = File.objects.get(file=file_name)

    # validating if the user requesting the file is from the same room where the file is available
    if requested_file.room.rname == request.session["rname"]:
        link = generate_presigned_url(file_name)
        return redirect(link)
    return HttpResponse("File not found")
