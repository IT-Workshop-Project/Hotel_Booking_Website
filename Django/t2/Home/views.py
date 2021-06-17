from django import contrib
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import HotelModel , Book
from datetime import date

# Create your views here.
def homePage(request):
    if request.method == 'POST':
        pass
    else:
        return render(request, "index.html",{})

def page2(request):
    context = {'hotels': HotelModel.objects.all()}
    return render(request, "2.html",context)

def page3(request):
    return render(request, "page.html",{})

def page4(request):
    return render(request, "silverhotel.html",{})
    
def adminloginview(request):
    return render(request, "login.html")

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
        return redirect(adminloginview)

def adminhomepage(request):
    if not request.user.is_authenticated:
        return redirect(adminloginview)
    

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
    date1 = date1.split('-')
    date2 = date2.split('-')
    d1=int(date1[2])
    d2=int(date2[2])

    days = d2-d1
    # name=request.HotelModel.name
    # for hotel in HotelModel.objects.all():
    #     hotell = hotel.id
    #     spechotel = HotelModel.objects.filter(id=hotell)

    for hotel in HotelModel.objects.all():
        hotelid = hotel.id
        price = hotel.price
        price = int(price)
        totalprice1 = days*(price)*(adult+children)
        totalprice1 = int(totalprice1)
        hotel.totalprice = totalprice1

        # for hotel in HotelModel.objects.filter(id=hotelid):
        #     idhotel = hotel.id
        #     hotel.totalprice = totalprice1
            # HotelModel(totalprice = totalprice1).save()
    print(hotel.totalprice)
    # price = days*(adult*price + children*price)
    context = {'hotels': HotelModel.objects.all()}
    return render(request,'2.html', context)

def add(request):
    name = request.POST['hotel']
    price = request.POST['price']
    image = request.FILES['imagename']

    HotelModel(name = name, price = price, totalprice = 0, hotel_Main_Img = image).save()
    return redirect(adminhomepage)  # Why not return render(adminhomepage)

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
        messages.add_message (request, messages.ERROR, "User Successfully created")
    
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
        messages.add_message(request, messages.SUCCESS,'Please log in first')
        return redirect(homePage)

    username = request.user.username
    bookedhotel = ''
    # id = hotelp
    context = {'hotels':HotelModel.objects.filter(id=hotelp)}
    
    # for hotel in HotelModel.objects.all():
    #     hotelid = hotel.id
    #     name = hotel.name
    #     price = hotel.price
    #     quantity = request.POST.get(str(hotelid),' ')
    
    #     if str(quantity)!='0' and str(quantity)!=' ':
    #         bookedhotel = bookedhotel + name + ' ' + price + 'quantity: '+ quantity

    for hotel in HotelModel.objects.filter(id=hotelp):
        hotelid = hotel.id
        name = hotel.name
        price = hotel.price
    
    Book(username = username, name = name).save()
    messages.add_message(request, messages.SUCCESS,'Booked Successfully')
    return redirect(customerwelcome)  # What if I don't return

def userbooking(request):
    bookings = Book.objects.filter(username = request.user.username)
    context = {'bookings': bookings }
    return render(request,'userbooking.html',context)

def specifichotel(request,hotelp):
    context = {'hotels':HotelModel.objects.filter(id=hotelp)}
    return render(request, 'page.html', context)
  
def success(request):
    return HttpResponse('successfully uploaded')

def display_hotel_images(request):
    if request.method == 'GET':
        # getting all the objects of hotel.
        Hotels = HotelModel.objects.all() 
        return render(request, 'display_hotel_images.html',{'hotel_images' : Hotels})