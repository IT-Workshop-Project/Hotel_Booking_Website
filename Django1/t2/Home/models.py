from django.db import models

from django import forms
from .models import *

# Create your models here.
class HotelModel(models.Model):
    name = models.CharField(max_length=20)
    price = models.CharField(max_length=5)
    hotel_Main_Img = models.ImageField(upload_to='images/')

class Book(models.Model):
    username = models.CharField(max_length=20)
    bookedhotel = models.CharField(max_length=20)
    name = models.CharField(max_length=20)

class HotelForm(forms.ModelForm):
    class Meta:
        model = HotelModel
        fields = ['hotel_Main_Img']