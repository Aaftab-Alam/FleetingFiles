from django import forms
from .models import Room


class CreateRoom(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['rname', 'rpass']


class LoginRoom(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['rname', 'rpass']
