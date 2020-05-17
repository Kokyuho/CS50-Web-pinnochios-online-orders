from django.contrib import admin

from .models import Pizza, Topping, Sub, SubExtra, Pasta, Salad, DinnerPlatter, Size, Profile, SubType, DinnerPlatterType, PizzaType, Product, ShoppingCart2, Quantity2


# Change the header
admin.site.site_header = "Pinnochio’s Pizza & Subs, Admin"


# markComplete method for admin
def markComplete(modeladmin, request, queryset):
    queryset.update(status="Complete")


# markPending method for admin
def markPending(modeladmin, request, queryset):
    queryset.update(status="Pending")


# Define shopping cart admin page
class ShoppingCart2Admin(admin.ModelAdmin):
    list_display = ("id" , "user", "status")
    list_filter = ("status",)
    fields = ("user", "status", "order_details")
    readonly_fields = ("order_details",)
    actions=[markComplete, markPending]

# Register pages
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
admin.site.register(ShoppingCart2, ShoppingCart2Admin)
admin.site.register(Quantity2)
admin.site.register(Product)




