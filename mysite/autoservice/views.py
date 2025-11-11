from django.shortcuts import render, reverse
from .models import Service, Car, Order, OrderLine, CustomUser
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin
from .forms import OrderCommentForm, CustomUserChangeForm, CustomUserCreateForm

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


class OrderDetailView(FormMixin, generic.DetailView):
    model = Order
    template_name = "order.html"
    context_object_name = "order"
    form_class = OrderCommentForm

    def get_success_url(self):
        return reverse("order", kwargs={"pk": self.object.pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.order = self.get_object()
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


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
    form_class = CustomUserCreateForm
    template_name = "signup.html"
    success_url = reverse_lazy("login")


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = "profile.html"
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user


class OrderCreateView(LoginRequiredMixin, generic.CreateView):
    model = Order
    template_name = "order_form.html"
    success_url = reverse_lazy('myorders')
    fields = ['car', 'status', 'deadline']

    def form_valid(self, form):
        form.instance.client = self.request.user
        form.save()
        return super().form_valid(form)


class OrderUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Order
    template_name = "order_form.html"
    fields = ['car', 'status', 'deadline']
    # success_url = reverse_lazy('myorders')

    def get_success_url(self):
        return reverse("order", kwargs={"pk": self.object.pk})

    def test_func(self):
        return self.get_object().client == self.request.user

class OrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Order
    template_name = "order_delete.html"
    context_object_name = "order"
    success_url = reverse_lazy('myorders')

    def test_func(self):
        return self.get_object().client == self.request.user