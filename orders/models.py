from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# User profile model
class Profile(models.Model):
      user = models.OneToOneField(User, on_delete=models.CASCADE)
      address = models.CharField(max_length=64, blank=True)
      phone = models.CharField(max_length=64, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
      if created:
            Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
      instance.profile.save()


# Product model
class Product(models.Model):
    name = models.CharField(max_length=64)
    size = models.CharField(max_length=64)
    price = models.FloatField()

    def __str__(self) -> str:
        return f"{self.name}, {self.size} - {self.price}"


# User shopping cart model (old)
class ShoppingCart(models.Model):
      user = models.OneToOneField(User, on_delete=models.CASCADE)
      items = models.ManyToManyField(Product)


# User shopping cart model
class ShoppingCart2(models.Model):
      user = models.ForeignKey(User, on_delete=models.CASCADE)
      items = models.ManyToManyField(Product, through="Quantity2")
      status = models.CharField(max_length=64, default='Active')

      def order_details(self):
        return "\n".join([(str(self.quantity2_set.get(product=p).quantity) + "x " +
                        p.name + " - " + p.size + " - Comments:" +
                        str(self.quantity2_set.get(product=p).comments)) for p in self.items.all()])


class Quantity2(models.Model):
      product = models.ForeignKey(Product, on_delete=models.CASCADE)
      shoppingCart = models.ForeignKey(ShoppingCart2, on_delete=models.CASCADE)
      quantity = models.IntegerField()
      comments = models.CharField(max_length=100, default='')


# # Order model
# class Order(models.Model):
#       user = models.ForeignKey(User, on_delete=models.CASCADE)
#       items = models.ManyToManyField(Item)
#       totalPrice = models.FloatField()

#       def __str__(self) -> str:
#             return f"{self.name}, {self.size} - {self.price}"


# Size Model
class Size(models.Model):
      size = models.CharField(max_length=64)

      def __str__(self):
            return self.size


# Pizza Model

class PizzaType(models.Model):
      pizzaType = models.CharField(max_length=64)
      
      def __str__(self):
            return f"{self.id} - {self.pizzaType}"

class Pizza(models.Model):
      pizzaType = models.ForeignKey(PizzaType, on_delete=models.DO_NOTHING)
      pizzaSize = models.ForeignKey(Size, on_delete=models.DO_NOTHING)
      price = models.FloatField()

      def __str__(self):
            return f"{self.id} - {self.pizzaType}, {self.pizzaSize} - {self.price}"


# Topping Model
class Topping(models.Model):
      name = models.CharField(max_length=64)

      def __str__(self):
            return f"{self.id} - {self.name}"


# Sub Model

class SubType(models.Model):
      subType = models.CharField(max_length=64)

      def __str__(self):
            return f"{self.id} - {self.subType}"

class Sub(models.Model):
      subType = models.ForeignKey(SubType, on_delete=models.DO_NOTHING)
      subSize = models.ForeignKey(Size, on_delete=models.DO_NOTHING)
      price = models.FloatField()

      def __str__(self):
            return f"{self.id} - {self.subType}, {self.subSize} - {self.price}"


# Sub Extra Model
class SubExtra(models.Model):
      extraType = models.CharField(max_length=64)
      price = models.FloatField()

      def __str__(self):
            return f"{self.id} - {self.extraType} - {self.price}"


# Pasta Model
class Pasta(models.Model):
      name = models.CharField(max_length=64)
      price = models.FloatField()

      def __str__(self):
            return f"{self.id} - {self.name} - {self.price}"


# Salad Model
class Salad(models.Model):
      name = models.CharField(max_length=64)
      price = models.FloatField()

      def __str__(self):
            return f"{self.id} - {self.name} - {self.price}"


# Dinner Platter Model

class DinnerPlatterType(models.Model):
      name = models.CharField(max_length=64)

      def __str__(self):
            return f"{self.id} - {self.name}"

class DinnerPlatter(models.Model):
      name = models.ForeignKey(DinnerPlatterType, on_delete=models.DO_NOTHING)
      size = models.ForeignKey(Size, on_delete=models.DO_NOTHING)
      price = models.FloatField()

      def __str__(self):
            return f"{self.id} - {self.name}, {self.size} - {self.price}"
