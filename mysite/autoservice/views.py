from django.shortcuts import render
from .models import Service, Car, Order, OrderLine
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

def index(request):
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    context = {
        'num_services': Service.objects.count(),
        'num_cars': Car.objects.count(),
        'num_orders_completed': Order.objects.filter(status='o').count(),
        'num_visits': num_visits,
    }
    return render(request, template_name="index.html", context=context)

def cars(request):
    cars = Car.objects.all()
    paginator = Paginator(cars, per_page=2)
    page_number = request.GET.get('page')
    paged_cars = paginator.get_page(page_number)
    return render(request, template_name="cars.html", context={"cars": paged_cars})

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


def search(request):
    query = request.GET.get('query')

    car_search_results = Car.objects.filter(Q(make__icontains=query) |
                                            Q(model__icontains=query) |
                                            Q(client_name__icontains=query) |
                                            Q(vin_code__icontains=query) |
                                            Q(license_plate__icontains=query))


    context = {
        "query": query,
        "cars": car_search_results,
    }
    return render(request, template_name="search.html", context=context)

class UserOrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = "myorders.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user)


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    template_name = "signup.html"
    success_url = reverse_lazy("login")

