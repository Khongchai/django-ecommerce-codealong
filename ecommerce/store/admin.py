from django.contrib import admin
from .models import Customer, Product, ShippingAddress, Cart, ItemInCart 

# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(ItemInCart)
admin.site.register(Cart)
admin.site.register(ShippingAddress)
