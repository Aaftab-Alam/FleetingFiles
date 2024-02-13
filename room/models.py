from django.db import models

"""
Models for the room app.

This module defines the models for the room app, including the Room and File models.

Classes:
- Room: Represents a room with a name and password.
- File: Represents a file uploaded to a room.

"""


class Room(models.Model):
    rname = models.CharField(max_length=30, unique=True)
    rpass = models.CharField(max_length=30)

class File(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    file = models.FileField()
    uploaded_at = models.DateTimeField(auto_now_add=True)