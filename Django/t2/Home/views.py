# from Home.models import PizzaModel
from django import contrib
from django.http import request
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import HotelModel , Book

# Create your views here.
def homePage(request):
    if request.method == 'POST':
        pass
    else:
        return render(request, "index1.html",{})

def page2(request):
        context = {'hotels': HotelModel.objects.all()}
        return render(request, "website2.html",context)

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
    context = {'price': adult*500 + children*300, 'hotels': HotelModel.objects.all() }
    return render(request,'website2.html',context)

def add(request):
    name = request.POST['pizza']
    price = request.POST['price']
    HotelModel(name = name, price = price).save()
    return redirect(adminhomepage)  # Why not return render(adminhomepage)

def delete(request,hotelpk):
    HotelModel.objects.filter(id = hotelpk).delete()
    return redirect(adminhomepage)

def usersignup(request):
        return render(request,'signupuser.html')

def signupuser(request):
    username = request.POST['email']
    password = request.POST['password']

    if User.objects.filter(username = username).exists():
        messages.add_message(request, messages.ERROR, "User already exists")
        return redirect(homePage)

    User.objects.create_user(username = username , password = password ).save()
    messages.add_message (request, messages.ERROR, "User Successfully created")
    return redirect(homePage)

def userlogin(request):
    return render(request,"userlogin.html")

def userauthenticate(request):
    username = request.POST['email']
    password = request.POST['password']

    user = authenticate( username = username, password = password )

    if user is not None:
        login(request,user)
        return redirect(customerwelcome)

    if user is None:
        messages.add_message(request,messages.ERROR,"Invalid Credentials")
        return redirect(userlogin)

def customerwelcome(request):
    if not request.user.is_authenticated:
        return redirect(homePage)

    username = request.user.username
    context = {'username':username, 'hotels': HotelModel.objects.all()}
    return render(request,'customerwelcome.html',context)

def book(request):
    username = request.user.username
    bookedhotel = ''

    for hotel in HotelModel.objects.all():
        hotelid= hotel.id
        name =hotel.name
        price = hotel.price
        quantity = request.POST.get(str(hotelid),' ')

        if str(quantity)!='0' and str(quantity)!=' ':
            bookedhotel = bookedhotel + name + ' ' + price + 'quantity: '+ quantity 
    
    Book( username = username, bookedhotel= bookedhotel).save()
    messages.add_message(request, messages.SUCCESS,'Booked Successfully')
    return redirect(customerwelcome)  # What if I don't return

def userbooking(request):
    bookings = Book.objects.filter( username = request.user.username)
    context = {'bookings': bookings}
    return render(request,'userbooking.html',context)

def specifichotel(request,hotelp):
    context = { 'hotels':HotelModel.objects.filter(id= hotelp)}
    return render(request, 'page.html', context)