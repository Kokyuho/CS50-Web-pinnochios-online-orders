from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Pizza, Topping, Sub, SubExtra, Pasta, Salad, DinnerPlatter, Size, Profile, SubType, DinnerPlatterType, PizzaType, Product, ShoppingCart2, Quantity2
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from django.core.mail import send_mail
from django.conf import settings
import stripe
import json
import os
# from django import forms

stripe.api_key = settings.STRIPE_SECRET_KEY

# METHODS
# Get user cart method
def getUserCart(user_id):
    cart = ShoppingCart2.objects.filter(status = "Active").get(user__exact = user_id)
    return cart

# Add user method for register form
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

    # Crete user shopping cart
    ShoppingCart2.objects.create(user=user)

    print('Successfully added user: ', username)

    return render(request, "orders/login.html", {"message": "User succesfully registered!"})

# Add to Cart method for ajax call in index
@csrf_exempt
def addToCart(request):
    
    # Query for ajax post request content
    data = request.POST.copy()
    username = data.get("username")
    name = data.get("name")
    size = data.get("size")
    comments = data.get("comments")

    # Get user id
    user_id = User.objects.get(username__exact=username).id

    # Get user's shopping cart
    cart = getUserCart(user_id)

    # Get item to be added
    if size != "None":
        # print(name)
        # print(Product.objects.filter(name = name))
        # print(size)
        # print(Product.objects.filter(name = name).get(size = size))
        item = Product.objects.filter(name = name).get(size = size)
    else:
        item = Product.objects.get(name = name)

    # For debugging
    # print('trying to add the following item: ', item)

    # Query user's cart to see if that item is already existent and in which quantity
    try:
        if size != "None":
            product = cart.items.filter(name=name).get(size=size)
        else:
            product = cart.items.get(name=name)
        
        # If the product exists in the user's cart, add one to the quantity
        quantity = cart.quantity2_set.get(product=product)
        quantity.quantity += 1
        quantity.save()
        quantity_value = quantity.quantity

    # # If it doesn't, add item and set quantity to 1.
    except Product.DoesNotExist:
        cart.items.add(item, through_defaults={'quantity': 1})
        quantity_value = 1

    # Add comments to the mix
    if size != "None":
        product = cart.items.filter(name=name).get(size=size)
    else:
        product = cart.items.get(name=name)
    quantity2_object = cart.quantity2_set.get(product=product)
    quantity2_object.comments += str(quantity_value) + ":" + comments
    allComments = quantity2_object.comments
    quantity2_object.save()

    # Print added item
    print('Added item ' + str(item) + ' to ' +  str(username) + \
        '\'s cart. Quantity = ' + str(quantity_value) + \
        ' Comments = ' + str(allComments))

    # Print user's shopping cart contents (for debugging)
    # cartContents = cart.items.all()
    # print(cartContents)
    
    return JsonResponse({'success': True})

# Increase cart count
@csrf_exempt
def increaseCartCount(request):

    # Get user id
    user_id = request.user

    # Get user's shopping cart
    cart = getUserCart(user_id)

    # Query user's cart to see whats the count
    items = cart.items.all()
    count = 0
    for item in items:
        quantity = cart.quantity2_set.get(product=item).quantity
        count += quantity

    # Send new value
    return JsonResponse({'badge': count})

# Decrease cart count
@csrf_exempt
def decreaseCartCount(request):

    # Get user id
    user_id = request.user

    # Get user's shopping cart
    cart = getUserCart(user_id)

    # Query user's cart to see whats the count
    items = cart.items.all()
    count = 0
    for item in items:
        quantity = cart.quantity2_set.get(product=item).quantity
        count += quantity

    # Send new value
    return JsonResponse({'badge': count})

# Delete item from cart
@csrf_exempt
def delItemFromCart(request):

    # Get user id
    user_id = request.user

    # Query for ajax post request content
    data = request.POST.copy()
    name = data.get("name")
    size = data.get("size")

    # Get user's shopping cart
    cart = getUserCart(user_id)

    # Delete item from cart
    try:
        product = cart.items.filter(name=name).get(size=size)
        cart.items.remove(product)
        # product.delete()
        print(f"{name}, {size} deleted from cart")
    except:
        print("There was an error deleting product")

    cart.save()

    # Get all cart items, their quantities and total
    items = cart.items.all()
    total = 0
    count = 0
    for item in items:
        quantity = cart.quantity2_set.get(product=item).quantity
        item.quantity = quantity
        item.totalPriceItem = item.price * quantity
        total += item.totalPriceItem
        count += quantity

    # Send response
    return JsonResponse({
        "success": True,
        "total": total,
        "badge": count
        })

# Substract item from cart
@csrf_exempt
def minusItemFromCart(request):

    # Get user id
    user_id = request.user

    # Query for ajax post request content
    data = request.POST.copy()
    name = data.get("name")
    size = data.get("size")

    # Get user's shopping cart
    cart = getUserCart(user_id)

    # Minus item from cart
    try:
        product = cart.items.filter(name=name).get(size=size)

        # If the product exists in the user's cart, substract one to the quantity
        quantity = cart.quantity2_set.get(product=product)
        quantity.quantity -= 1
        quantity.save()
        quantity_value = quantity.quantity

        # Calculate new item total price
        newTotalPriceItem = product.price * quantity.quantity

    except:
        print("There was an error substracting product")

    # Get all cart items, their quantities and total
    items = cart.items.all()
    total = 0
    for item in items:
        quantity = cart.quantity2_set.get(product=item).quantity
        item.quantity = quantity
        item.totalPriceItem = item.price * quantity
        total += item.totalPriceItem

    # Send response
    return JsonResponse({
        "quantity": quantity_value,
        "newTotalPriceItem": newTotalPriceItem,
        "total": total
        })

# Delete item from cart
@csrf_exempt
def plusItemFromCart(request):

    # Get user id
    user_id = request.user

    # Query for ajax post request content
    data = request.POST.copy()
    name = data.get("name")
    size = data.get("size")

    # Get user's shopping cart
    cart = getUserCart(user_id)

    # Plus item from cart
    try:
        product = cart.items.filter(name=name).get(size=size)

        # If the product exists in the user's cart, add one to the quantity
        quantity = cart.quantity2_set.get(product=product)
        quantity.quantity += 1
        quantity.save()
        quantity_value = quantity.quantity

        # Calculate new item total price
        newTotalPriceItem = product.price * quantity.quantity

    except:
        print("There was an error adding product")

    # cart.save()

    # Get all cart items, their quantities and total
    items = cart.items.all()
    total = 0
    for item in items:
        quantity = cart.quantity2_set.get(product=item).quantity
        item.quantity = quantity
        item.totalPriceItem = item.price * quantity
        total += item.totalPriceItem

    # Send response
    return JsonResponse({
        "quantity": quantity_value,
        "newTotalPriceItem": newTotalPriceItem,
        "total": total
        })

# Create payment intent method for stripe (card payments)
@csrf_exempt
def createPaymentIntent(request):

    # Check if user is logged in
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None})

    # Get user id
    user_id = request.user

    # Get user's shopping cart
    cart = getUserCart(user_id)

    # If shopping cart is empty, inform the user
    if not cart.items.all():
        return render(request, "orders/shoppingCart.html", {"message": "Your shopping cart is still empty!"})

    # Get user's shopping cart
    cart = ShoppingCart2.objects.filter(status = "Active").get(user__exact = user_id)

    # Get all cart items, their quantities and total
    items = cart.items.all()
    count = 0
    total = 0
    for item in items:
        quantity = cart.quantity2_set.get(product=item).quantity
        item.quantity = quantity
        item.totalPriceItem = item.price * quantity
        total += item.totalPriceItem
        count += quantity

    
    try:
        # Create intent
        intent = stripe.PaymentIntent.create(
            amount=int(total*100),
            currency='usd'
        )
        return JsonResponse({ 'clientSecret': intent['client_secret'] })

    except Exception as e:
        return JsonResponse({ 'error': str(e)}, status=403)


# VIEWS
# Index view
def index(request):

    # Get user id
    user_id = request.user

    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None})

    # Get user's shopping cart
    cart = getUserCart(user_id)

    # Query user's cart to see whats the count
    items = cart.items.all()
    count = 0
    for item in items:
        quantity = cart.quantity2_set.get(product=item).quantity
        count += quantity
    
    context = {
        "user": request.user,
        "pizzaTypes": PizzaType.objects.all(),
        "subTypes": SubType.objects.all(),
        "pastaTypes": Pasta.objects.all(),
        "saladTypes": Salad.objects.all(),
        "dinnerPlatterTypes": DinnerPlatterType.objects.all(),
        "toppings": Topping.objects.all(),
        "subExtras": SubExtra.objects.all(),
        "products": Product.objects.all(),
        "badge": count
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

# Shopping Cart view
def shoppingCart(request):

    # Check if user is logged in
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None})

    # Get user id
    user_id = request.user

    # Get user's shopping cart
    cart = getUserCart(user_id)

    # # Query user's cart to see whats the count
    # count = cart.items.all().count()

    # Get all cart items, their quantities and total
    items = cart.items.all()
    count = 0
    total = 0
    for item in items:
        quantity = cart.quantity2_set.get(product=item).quantity
        item.quantity = quantity
        item.totalPriceItem = item.price * quantity
        total += item.totalPriceItem
        count += quantity
    # total = cart.items.aggregate(Sum('price'))['price__sum']

    # Create context
    context = {
        "user": request.user,
        "pizzaTypes": PizzaType.objects.all(),
        "subTypes": SubType.objects.all(),
        "pastaTypes": Pasta.objects.all(),
        "saladTypes": Salad.objects.all(),
        "dinnerPlatterTypes": DinnerPlatterType.objects.all(),
        "toppings": Topping.objects.all(),
        "subExtras": SubExtra.objects.all(),
        "badge": count,
        "items": items,
        "total": total
    }

    # Render shopping cart template
    return render(request, "orders/shoppingCart.html", context)

# Checkout view
def checkout(request):
    
    # Check if user is logged in
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None})

    # Get user id
    user_id = request.user

    # Get user's shopping cart
    cart = getUserCart(user_id)

    # If shopping cart is empty, inform the user
    if not cart.items.all():
        return render(request, "orders/shoppingCart.html", {"message": "Your shopping cart is still empty!"})

    # Get user's shopping cart
    cart = ShoppingCart2.objects.filter(status = "Active").get(user__exact = user_id)

    # Get all cart items, their quantities and total
    items = cart.items.all()
    count = 0
    total = 0
    for item in items:
        quantity = cart.quantity2_set.get(product=item).quantity
        item.quantity = quantity
        item.totalPriceItem = item.price * quantity
        total += item.totalPriceItem
        count += quantity

    # Create context
    context = {
        "user": request.user,
        "badge": count,
        "total": total
    }

    # Render checkout template
    return render(request, "orders/checkout.html", context)

# Order Placed view
def orderPlaced(request):
    
    # Get user id
    user_id = request.user

    # Get user's shopping cart
    cart = getUserCart(user_id)

    # Change cart status to confirmed
    cart.status = "Confirmed"
    cart.save()

    # Create a new shopping cart for the user and make it the active one
    ShoppingCart2.objects.create(user=user_id)

    # Get user's shopping cart
    cart = ShoppingCart2.objects.filter(status = "Active").get(user__exact = user_id)

    # Get all cart items, their quantities and total
    items = cart.items.all()
    count = 0
    total = 0
    for item in items:
        quantity = cart.quantity2_set.get(product=item).quantity
        item.quantity = quantity
        item.totalPriceItem = item.price * quantity
        total += item.totalPriceItem
        count += quantity

    # Create context
    context = {
        "user": request.user,
        "badge": count,
    }

    # Render order confirmed template
    return render(request, "orders/orderConfirmed.html", context)

# Orders view
def orders(request):

    # Check if user is logged in
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None})

    # Get user id
    user_id = request.user

    # Get all user's non active shopping carts
    carts = ShoppingCart2.objects.exclude(status = "Active")

    # Count all items in active cart for badge
    cart = getUserCart(user_id)
    items = cart.items.all()
    count = 0
    total = 0
    for item in items:
        quantity = cart.quantity2_set.get(product=item).quantity
        item.quantity = quantity
        item.totalPriceItem = item.price * quantity
        total += item.totalPriceItem
        count += quantity

    # Create context
    context = {
        "user": request.user,
        "badge": count,
        "carts": carts
    }

    # Render shopping cart template
    return render(request, "orders/orders.html", context)

