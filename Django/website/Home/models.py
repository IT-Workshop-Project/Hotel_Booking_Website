from django.db import models

from django import forms
from django.db.models.base import Model
from .models import *

# Create your models here.
class HotelModel(models.Model):
    name = models.CharField(max_length=20)
    price = models.CharField(max_length=5)
    hotel_Main_Img = models.ImageField(upload_to='images/')
    hotel_Main_Img1 = models.ImageField(upload_to='images/')
    hotel_Main_Img2 = models.ImageField(upload_to='images/')
    hotel_Main_Img3 = models.ImageField(upload_to='images/')
    totalprice = models.CharField(max_length=10)

class Book(models.Model):
    username = models.CharField(max_length=20)
    bookedhotel = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    Hotel_image = models.ImageField(upload_to='images/')