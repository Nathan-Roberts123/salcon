from typing import Any, Dict
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic.edit import FormView
from .models import products, Address, orderItem, country
from .forms import registerForm, addressForm
from django.contrib.auth import authenticate, login, logout
import json

from .utils import say, getTotalItems, getCartOrders, getFullTotal, getFinalOrder, getAddresses, get_totalOrders
from django.conf import settings

import stripe

stripe.api_key = settings.STRIPE_PRIVATE_KEY

shipping_cost = 200

user_total_amnt = 0
guest_total_amnt = 0

class homePage(ListView):
    template_name = "base/Home.html"
    model = products
    context_object_name = 'products'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            user_orders = orderItem.objects.filter(cumstomer = self.request.user)
            context["cart_total"] = get_totalOrders(user_orders)
        
        else:
            context["cart_total"] = getTotalItems(self.request)
        
        return context
    
    def get(self, request, *args, **kwargs):
        getTotalItems(request)
        return super().get(request, *args, **kwargs)
    
class regesterFormView(FormView):
    template_name = "base/register.html"
    form_class = registerForm
    success_url = "/"

    def form_valid(self, form):
        form.save()
        email=form.cleaned_data['email']
        password=form.cleaned_data['password1']

        user = authenticate(email=email, password=password)
        login(self.request, user)

        return super().form_valid(form)
    
    def form_invalid(self, form):
        print("an error occured during regitration")
        return super().form_invalid(form)
    
    

class addressFormView(FormView):
    template_name = "base/add_address.html"
    form_class = addressForm
    success_url = "/payment/"

    def form_valid(self, form):
        form.instance.person = self.request.user
        form.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print("an error occured during address creation")
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        countries = country.objects.all()

        if self.request.user.is_authenticated:
            user_orders = orderItem.objects.filter(cumstomer = self.request.user)
            context["cart_total"] = get_totalOrders(user_orders)
        else:
            context["cart_total"] = len(say(self.request))
            context["countries"] = countries
 

        return context



def loginPage(request):

    if request.method == "POST":
        user_email = request.POST['email']
        user_password = request.POST['password']
        user = authenticate(request, email=user_email, password=user_password)

        print("email: ", user_email)
        print("password: ", user_password)
        print("user: ", user)

        if user is not None:
            login(request, user)
            return redirect("home-page")
        
        else:
            print("can not log you in")
            return redirect("login")
    
    else:
        return render(request, "base/login.html")
    
def logoutPage(request):
    logout(request)
    return render(request, "base/logout.html")

def checkout(request):

    context = {}
    total_price = 0
    if request.user.is_authenticated:
        user_orders = orderItem.objects.filter(cumstomer = request.user)
        user_products = []

        for user_order in user_orders:
            total_price += user_order.Total()
            user_products.append({"product": user_order.product, "quantity":user_order.quantity, "Total":user_order.Total})

        context = {"cart_total": get_totalOrders(user_orders), "cart_orders":user_products, "total_price":total_price }
    else:
        context = {"cart_total": getTotalItems(request), "cart_orders": getFinalOrder(request), "total_price": getFullTotal(request)}
    


    return render(request, "base/check_out.html", context)


def payment(request):

    total_price = 0
    user_orders = []
    addresses = []

    if request.user.is_authenticated:
        user_orders = orderItem.objects.filter(cumstomer = request.user)
        addresses = Address.objects.filter(person = request.user)

        for user_order in user_orders:
            total_price += user_order.Total()
        
        context = {"addresses":addresses, "cart_total": get_totalOrders(user_orders), "orders":user_orders, "total_price":total_price, "total_payable":total_price + shipping_cost, "shipping_cost": shipping_cost, "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY}

    else:
        context = {"addresses":getAddresses(request), "cart_total":getTotalItems(request), "orders": getFinalOrder(request), "shipping_cost": shipping_cost, "total_price": getFullTotal(request), "total_payable": getFullTotal(request) + shipping_cost, "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY}


    return render(request, "base/payment.html", context)


def addToCart(request):
    if request.method == "POST":
        res_data = json.loads(request.body)
        print(res_data)

        p_product = products.objects.get(name = res_data["product"])

        if res_data['action'] == "create":
            try:
                t_order = orderItem.objects.get(product=p_product, cumstomer=request.user)
                t_order.quantity += 1
                t_order.save()

            except:
                order = orderItem.objects.create(product=p_product, cumstomer=request.user, quantity=1)

        elif res_data['action'] == "add":
            o_order = orderItem.objects.get(product=p_product, cumstomer=request.user)
            o_order.quantity += 1
            o_order.save()

        elif res_data['action'] == "remove":
            oo_order = orderItem.objects.get(product=p_product, cumstomer=request.user)
            oo_order.quantity -= 1
            oo_order.save()

            if oo_order.quantity == 0:
                oo_order.delete()


        return JsonResponse("successfull updated cart", safe=False)

def secret(request):

    if request.method == "POST":
        if request.user.is_authenticated:
            amnt = shipping_cost
            user_orders = orderItem.objects.filter(cumstomer = request.user)
    
            for user_order in user_orders:
                amnt += user_order.Total()
            
            print("amount: ", amnt)

        else:
            amnt = getFullTotal(request) + shipping_cost
        
        try:
            gcustomer = stripe.Customer.create()
            intent = stripe.PaymentIntent.create(
                    amount = int(amnt * 100),
                    currency = "usd",
                    customer = gcustomer["id"]
            )

            return JsonResponse({"clientSecret": intent["client_secret"]})
        except Exception as e:
            return JsonResponse({"error":str(e)})