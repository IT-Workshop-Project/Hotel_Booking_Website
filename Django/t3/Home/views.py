from django import contrib
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import HotelModel , Book
from datetime import datetime

# Create your views here.
def homePage(request):
    if request.method == 'POST':
        pass
    else:
        return render(request, "index.html",{})

def page2(request):
    context = {'hotels': HotelModel.objects.all()}
    return render(request, "hotels.html",context)

def logoutuser(request):
    logout(request)
    return redirect(homePage)

def authenticateadmin(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate( username = username, password = password )

    if user is not None:
        login(request,user)
        return redirect('adminhomepage')

    if user is None:
        messages.add_message(request,messages.ERROR,"Invalid Credentials")
        return redirect(homePage)

def adminhomepage(request):
    if not request.user.is_authenticated:
        return redirect(homePage)
    
    context = {'hotels': HotelModel.objects.all()}
    return render(request,"adminhomepage.html",context)

def redirecthomePage(request):
    return redirect(homePage)

def price(request):
    adult = request.POST['adult']
    children  = request.POST['Children']
    adult = int(adult)
    children = int(children)
    date1 = request.POST['check-in date']
    date2 = request.POST['check-out date']
    your_date_string1 = date1
    your_date_string2 = date2
    datetime_object1 = datetime.strptime(your_date_string1, "%Y-%m-%d")
    datetime_object2 = datetime.strptime(your_date_string2, "%Y-%m-%d")
    days1 = datetime_object2 - datetime_object1
    days = str(days1)

    # days = days.split(',')
    # days = days[0]
    # days = days.split(' ')
    # diff = days[0]
    # diff = int(diff)
    # print(diff)

    days=list(days)
    days[0]=int(str(days[0]+days[1]))
    diff=days[0]
    
    for hotel in HotelModel.objects.all():
        hotelid = hotel.id
        price = hotel.price
        price = int(price)
        totalprice1 = diff*(price)*(adult+children)
        totalprice1 = int(totalprice1)
        for p in HotelModel.objects.filter(id=hotelid):
            p.totalprice = totalprice1
            p.save()

    for a in HotelModel.objects.all():
        amt = hotel.totalprice
        for x in amt:
            if x<amt:
                x=amt
    
    context = {'hotels': HotelModel.objects.all(),'cheapest':HotelModel.objects.filter(totalprice = x)}
    return render(request,'hotels.html', context)

def add(request):
    name = request.POST['hotel']
    price = request.POST['price']
    image = request.FILES['imagename']
    image1 = request.FILES['image1']
    image2 = request.FILES['image2']
    image3 = request.FILES['image3']

    HotelModel(name = name, price = price, totalprice = 0, hotel_Main_Img = image, hotel_Main_Img1 = image1, hotel_Main_Img2 = image2, hotel_Main_Img3 = image3 ).save()
    return redirect(adminhomepage)

def delete(request,hotelpk):
    HotelModel.objects.filter(id = hotelpk).delete()
    return redirect(adminhomepage)

def signupuser(request):
    username = request.POST['email']
    password = request.POST['password']
    repass = request.POST['psw_repeat']

    if password == repass:
        if User.objects.filter(username = username).exists():
            messages.add_message(request, messages.ERROR, "User already exists")
            return redirect(homePage)

        User.objects.create_user(username = username, password = password ).save()
        messages.add_message (request, messages.SUCCESS, "User Successfully created")
    
    else:
        messages.add_message(request, messages.ERROR, "Password do not match")

    return redirect(homePage)

def userauthenticate(request):
    username = request.POST['email']
    password = request.POST['password']

    user = authenticate( username = username, password = password )

    if user is not None:
        login(request,user)
        return redirect(customerwelcome)

    if user is None:
        messages.add_message(request,messages.ERROR,"Invalid Credentials")
        return redirect(homePage)

def customerwelcome(request):
    if not request.user.is_authenticated:
        return redirect(homePage)

    username = request.user.username
    context = {'username':username, 'hotels': HotelModel.objects.all()}
    return render(request,'customerwelcome.html',context)

def book(request,hotelp):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR,'Please log in first')
        return redirect(homePage)

    username = request.user.username
    context = {'hotels':HotelModel.objects.filter(id=hotelp)}

    for hotel in HotelModel.objects.filter(id=hotelp):
        name = hotel.name
        price = hotel.price
        image = hotel.hotel_Main_Img

    Book(username = username, name = name, Hotel_image = image).save()
    messages.add_message(request, messages.SUCCESS,'Hotel Booked Successfully')
    return redirect(customerwelcome)

def userbooking(request):
    bookings = Book.objects.filter(username = request.user.username)
    context = {'bookings': bookings }
    return render(request,'userbooking.html',context)

def specifichotel(request,hotelp):
    context = {'hotels':HotelModel.objects.filter(id=hotelp)}
    return render(request, 'page1.html', context)

def cancel(request,bookid):
    messages.add_message(request, messages.ERROR, "Booking successfully cancelled")
    Book.objects.filter(id = bookid).delete()
    return redirect(userbooking)