from store.utils import get_cart_and_items
from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json


def store(request):
    products = Product.objects.all()
    context = get_cart_and_items(request)
    context["products"] = products
    return render(request, "store.html", context)

def cart(request):
    context = get_cart_and_items(request)
    return render(request, "cart.html", context)

def checkout(request):
    context = get_cart_and_items(request) 
    return render(request, "checkout.html", context)

def update_item(request):
    data = json.loads(request.body)
    product_id = data["productId"]
    action = data["action"]

    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    cart, _ = Cart.objects.get_or_create(customer=customer, complete=False)

    item_in_cart, _ = ItemInCart.objects.get_or_create(cart=cart, product=product)

    print("action is " + action)

    if action == "add":
        item_in_cart.quantity += 1
    elif action == "remove":
        item_in_cart.quantity -= 1
    item_in_cart.save()

    if item_in_cart.quantity < 1:
        item_in_cart.delete()

    #from docs, :param safe: Controls if only ``dict`` objects may be serialized. Defaults
    #to ``True``.
    return JsonResponse("Item was added", safe=False)