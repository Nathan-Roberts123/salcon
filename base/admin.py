from django.contrib import admin
from .models import products, User, country, Address, orderItem

# Register your models here.
admin.site.register(products)
admin.site.register(User)
admin.site.register(country)
admin.site.register(Address)
admin.site.register(orderItem)