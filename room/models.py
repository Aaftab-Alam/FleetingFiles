from django.db import models

class Room(models.Model):
    rname = models.CharField(max_length=30, unique=True)
    rpass = models.CharField(max_length=30)

class File(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)



