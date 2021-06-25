from .models import Cart

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
    else:
        items = []
        context["item"] = items
        
    return context