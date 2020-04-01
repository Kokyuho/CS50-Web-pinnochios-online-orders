from django.contrib import admin

from .models import Pizza, Topping, Sub, SubExtra, Pasta, Salad, DinnerPlatter, Size, Profile, SubType, DinnerPlatterType, PizzaType

# Register your models here.
admin.site.register(Pizza)
admin.site.register(Topping)
admin.site.register(Sub)
admin.site.register(SubExtra)
admin.site.register(Pasta)
admin.site.register(Salad)
admin.site.register(DinnerPlatter)
admin.site.register(Size)
admin.site.register(Profile)
admin.site.register(SubType)
admin.site.register(DinnerPlatterType)
admin.site.register(PizzaType)
