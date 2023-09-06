import json
from .models import products

def say(request):
    try:
        cart_products = json.loads(request.COOKIES['items'])
        return cart_products
    except Exception as e:
        return {}


def getTotalItems(request):
    product_list = say(request)
    total = 0

    for product in product_list:
        total += product_list[product]['quantity']

    return total

def getCartOrders(request):
    cart_orders = []
    product_list = say(request)

    for product in product_list:
        cart_orders.append(product)
    
    return cart_orders

def getFinalOrder(request):
    cart_orders = getCartOrders(request)
    product_list = say(request)
    cart_orders_objs = []


    for cart_order in cart_orders:
        prd = products.objects.get(name = cart_order)
        prd_price = prd.price

        qnt = product_list[cart_order]['quantity']

        cart_orders_objs.append({"product": prd, "quantity": qnt, "Total": qnt*prd_price})
    return cart_orders_objs


def getFullTotal(request):
    total_orders = getFinalOrder(request)
    total = 0

    for total_order in total_orders:
        total += total_order["Total"]
    
    return total


def getAddresses(request):
    try:
        address = json.loads(request.COOKIES['address'])
        return [address]
    except Exception as e:
        print("error:", e)
        return {}
    
def get_totalOrders(user_orders):
    total_orders = 0
    for user_order in user_orders:
        total_orders += user_order.quantity
    return total_orders








