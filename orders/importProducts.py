# This is to be run in django shell

from orders.models import Pizza, Topping, Sub, SubExtra, Pasta, Salad, DinnerPlatter, Size, Profile, SubType, DinnerPlatterType, PizzaType, Product, ShoppingCart2

# Add all pizzas
for pizza in Pizza.objects.all():
    Product.objects.create(
        name = "Pizza - " + pizza.pizzaType.pizzaType,
        size = pizza.pizzaSize.size,
        price = pizza.price
    )

# Add all subs
for sub in Sub.objects.all():
    Product.objects.create(
        name = "Sub - " + sub.subType.subType,
        size = sub.subSize.size,
        price = sub.price
    )

# Add all subs extras
for subExtra in SubExtra.objects.all():
    Product.objects.create(
        name = "SubExtra - " + subExtra.extraType,
        size = "",
        price = subExtra.price
    )

# Add all pastas
for pasta in Pasta.objects.all():
    Product.objects.create(
        name = "Pasta - " + pasta.name,
        size = "",
        price = pasta.price
    )

# Add all salads
for salad in Salad.objects.all():
    Product.objects.create(
        name = "Salad - " + salad.name,
        size = "",
        price = salad.price
    )

# Add all dinner platters
for dinnerPlatter in DinnerPlatter.objects.all():
    Product.objects.create(
        name = "Dinner Platter - " + dinnerPlatter.name.name,
        size = dinnerPlatter.size.size,
        price = dinnerPlatter.price
    )