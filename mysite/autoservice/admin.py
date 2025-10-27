from django.contrib import admin
from .models import Service, Car, Order, OrderLine

admin.site.register(Service)
admin.site.register(Car)
admin.site.register(Order)
admin.site.register(OrderLine)
