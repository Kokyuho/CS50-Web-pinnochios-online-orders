from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Pizza, Topping, Sub, SubExtra, Pasta, Salad, DinnerPlatter, Size, Profile, SubType, DinnerPlatterType, PizzaType
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# Index view
def index(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None})
    context = {
        "user": request.user,
        "pizzaTypes": PizzaType.objects.all(),
        "subTypes": SubType.objects.all(),
        "pastaTypes": Pasta.objects.all(),
        "saladTypes": Salad.objects.all(),
        "dinnerPlatterTypes": DinnerPlatterType.objects.all(),
        "toppings": Topping.objects.all(),
        "subExtras": SubExtra.objects.all()
    }
    return render(request, "orders/index.html", context)


# Login view
def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "orders/login.html", {"message": "Invalid credentials."})


# Logout view
def logout_view(request):
    logout(request)
    return render(request, "orders/login.html", {"message": "Logged out."})


# Register view
def register_view(request):
    return render(request, "orders/register.html", {"message": None})


# Logout view
def addUser(request):
    # Query for form data
    username = request.POST["username"]
    password = request.POST["password"]
    repeatPassword = request.POST["repeatPassword"]
    firstName = request.POST["firstName"]
    lastName = request.POST["lastName"]
    email = request.POST["email"]
    phone = request.POST["phone"]
    address = request.POST["address"]

    # Abort if password is not equal
    if password != repeatPassword:
        return render(request, "orders/register.html", {"message": "Error: Passwords given don't match."})

    # Create user and fill additional info
    user = User.objects.create_user(username, email, password)
    user.first_name = firstName
    user.last_name = lastName
    user.profile.phone = phone
    user.profile.address = address
    user.save()

    print('Successfully added user: ', username)
    print(user.profile.phone)

    return render(request, "orders/login.html", {"message": "User succesfully registered!"})


# Add to Cart view
def addToCart_view(request):
    return HttpResponseRedirect(reverse("index"))
