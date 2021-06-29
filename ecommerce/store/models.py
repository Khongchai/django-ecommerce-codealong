from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank = True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    #Don't ship if digital.
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try: 
            url = self.image.url
        except: 
            url = ""
        return url


#Cart can have multiple items in the cart.
class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    #If false, the cart is still open, user can continue adding items to the cart, else might have to create
    #items and add them to another cart. 
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return str(self.id)

    #You can call properties like they are properties, not functions, so no pair of parens at the end.
    @property
    def get_cart_total(self):
        itemsincart = self.itemincart_set.all()
        total = sum([item.get_total for item in itemsincart])
        return total

    @property
    def get_cart_items(self):
        itemsincart = self.itemincart_set.all()
        total = sum([item.quantity for item in itemsincart])
        return total

    #check if shipping is requried
    @property
    def shipping(self):
        shipping = False
        items_in_cart = self.itemincart_set.all()
        for item in items_in_cart:
            if not item.product.digital:
                shipping = True
        return shipping

#Think of this as a state of the item being in the cart
class ItemInCart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    cart =  models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name
    
    @property 
    def get_total(self):
        total = self.product.price * self.quantity
        return total



class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address