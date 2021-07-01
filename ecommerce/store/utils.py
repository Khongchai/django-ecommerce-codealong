from .models import Cart, Product
import json

def get_cart_and_items(request):
    context = {}
    if request.user.is_authenticated:
        customer = request.user.customer
        #Django's method of reducing boiler plate code of 
        #checking if something exist before creating or getting info
        # https://docs.djangoproject.com/en/3.2/ref/models/querysets/#get-or-create
        cart, _ = Cart.objects.get_or_create(customer=customer, complete=False)
        #get backward data with {nameofmodel_set}.all()
        items = cart.itemincart_set.all()
        context["cart"] = cart
        context["items"] = items
        context["items_in_cart"] = cart.get_cart_items
        context["shipping"] = cart.shipping
    else:

         #for first load
        try:
            returned_cart = json.loads(request.COOKIES['cart'])
        except:
            returned_cart = {}

        #start building out an order
        context["items"] = [] 
        cart = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
         
        for i in returned_cart:
            #Try catch is to make sure that the product we query for is indeed in the database
            #For example, when a product is deleted from the database after the user has selected it.
            try:
                product = Product.objects.get(id=i)
                total = (product.price * returned_cart[i]["quantity"])

                cart["get_cart_items"]+= returned_cart[i]["quantity"]
                cart["get_cart_total"] += total

                #the structure reflects what we set in javascript
                item = {
                    "product":{
                        "id": product.id,
                        "name": product.name,
                        "price": product.price,
                        "imageURL": product.imageURL
                    },
                    "quantity": returned_cart[i]["quantity"],
                    "get_total": total,
                }
            except:
                #Let this be the algorithm that fixes this
                pass

            if (not product.digital):
                cart["shipping"] = True

            context["items"].append(item)

        context["cart"] = cart
        context["items_in_cart"] = cart["get_cart_items"]
    return context