from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("cars/", views.cars, name="cars"),
    path("cars/<int:car_pk>/", views.car, name="car"),
    path("orders/", views.OrderListView.as_view(), name="orders"),
]
