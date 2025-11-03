from django.shortcuts import render
from .models import Service, Car, Order, OrderLine
from django.views import generic

def index(request):
    context = {
        'num_services': Service.objects.count(),
        'num_cars': Car.objects.count(),
        'num_orders_completed': Order.objects.filter(status='o').count(),
    }
    return render(request, template_name="index.html", context=context)

def cars(request):
    return render(request, template_name="cars.html", context={"cars": Car.objects.all()})

def car(request, car_pk):
    return render(request, template_name="car.html", context={"car": Car.objects.get(pk=car_pk)})

class OrderListView(generic.ListView):
    model = Order
    template_name = "orders.html"
    context_object_name = "orders"
    paginate_by = 2


class OrderDetailView(generic.DetailView):
    model = Order
    template_name = "order.html"
    context_object_name = "order"
