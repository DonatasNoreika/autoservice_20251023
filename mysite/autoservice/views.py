from django.shortcuts import render
from .models import Service, Car, Order, OrderLine

def index(request):
    context = {
        'num_services': Service.objects.count(),
        'num_cars': Car.objects.count(),
        'num_orders_completed': Order.objects.filter(status='o').count(),
    }
    return render(request, template_name="index.html", context=context)