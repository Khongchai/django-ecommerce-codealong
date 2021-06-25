from store.utils import get_cart_and_items
from django.shortcuts import render
from .models import *


def store(request):
    products = Product.objects.all()
    context = { 'products': products }
    return render(request, "store.html", context)

def cart(request):
    context = get_cart_and_items(request)

    return render(request, "cart.html", context)

def checkout(request):
    context = get_cart_and_items(request) 

    return render(request, "checkout.html", context)