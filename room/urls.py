from django.urls import path
from room import views

"""
URL patterns for the room app.

This module defines the URL patterns for the room app, which handles various actions related to rooms.

Functions:
- room(request): Renders the room view.
- create_room(request): Creates a new room.
- join_room(request): Joins an existing room.
- leave_room(request): Leaves a room.
- upload(request): Handles file uploads.
- download_file(request, file_name): Downloads a file from the media directory.
- delete_room(request): Deletes a room.

"""


urlpatterns = [
    path('', views.room, name="room"),
    path('create_room', views.create_room, name="create_room"),
    path('join_room', views.join_room, name="join_room"),
    path('leave_room', views.leave_room, name="leave_room"),
    path('upload', views.upload, name="upload"),
    path('media/file/<str:file_name>/', views.download_file, name='download_file'),
    path('delete_room', views.delete_room, name='delete_room'),
]