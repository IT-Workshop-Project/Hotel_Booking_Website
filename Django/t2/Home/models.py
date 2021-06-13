from django.db import models

# Create your models here.
class HotelModel(models.Model):
    name = models.CharField(max_length=20)
    price = models.CharField(max_length=5)

class Book(models.Model):
    username = models.CharField(max_length=20)
    bookedhotel = models.CharField(max_length=20)
