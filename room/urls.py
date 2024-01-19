from django.urls import path
from room import views


urlpatterns = [
    path('', views.room, name="upload"),
    path('create_room', views.create_room, name="create_room"),
    path('join_room', views.join_room, name="join_room"),


]