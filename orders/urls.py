from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("addUser", views.addUser, name="addUser"),
    path("addToCart", views.addToCart, name="addToCart"),
    path("increaseCartCount", views.increaseCartCount, name="increaseCartCount"),
    path("decreaseCartCount", views.increaseCartCount, name="decreaseCartCount"),
    path("shoppingCart", views.shoppingCart, name="shoppingCart"),
    path("delItemFromCart", views.delItemFromCart, name="delItemFromCart"),
    path("minusItemFromCart", views.minusItemFromCart, name="minusItemFromCart"),
    path("plusItemFromCart", views.plusItemFromCart, name="plusItemFromCart"),
    path("orderPlaced", views.orderPlaced, name="orderPlaced"),
    path("orders", views.orders, name="orders"),
    path("checkout", views.checkout, name="checkout"),
    path("createPaymentIntent", views.createPaymentIntent, name="createPaymentIntent")
]
