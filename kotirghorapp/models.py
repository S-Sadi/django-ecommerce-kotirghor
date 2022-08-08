from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

CATEGORY_CHOICES=(
    ("BP", "Bamboo Products"),
    ("CP", "Cane Products"),
    ("EP", "Earthenware")
)


class Item(models.Model):
    title = models.CharField(max_length=50)
    image_path = models.CharField(max_length=70)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    discription = models.CharField(max_length=150)
    price = models.FloatField()

    def get_add_to_cart(self):
        return reverse("addtocart", kwargs={"slug":self.id})

    def __str__(self) -> str:
        return self.title
    

class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.item.title
    
    def get_total_price(self) -> int:
        return self.quantity*self.item.price


class Order(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    items = models.ManyToManyField(OrderItem)

    def __str__(self) -> str:
        return self.user.username