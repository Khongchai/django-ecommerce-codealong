from django.shortcuts import render
from .models import *


def store(request):
    products = Product.objects.all()
    context = { 'products': products }
    return render(request, "store.html", context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        #Django's method of reducing boiler plate code of 
        #checking if something exist before creating or getting info
        # https://docs.djangoproject.com/en/3.2/ref/models/querysets/#get-or-create
        cart, _ = Cart.objects.get_or_create(customer=customer, complete=False)
        #get backward data with {nameofmodel_set}.all()
        items = cart.itemincart_set.all()
    else:
        items = []

    context = {"items" : items}  
    return render(request, "cart.html", context)

def checkout(request):
    context = {}
    return render(request, "checkout.html", context)