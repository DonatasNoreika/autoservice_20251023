from django.db import models


class Service(models.Model):
    name = models.CharField()
    price = models.FloatField()


class Car(models.Model):
    make = models.CharField()
    model = models.CharField()
    license_plate = models.CharField()
    vin_code = models.CharField()
    client_name = models.CharField()


class Order(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    car = models.ForeignKey(to="Car", on_delete=models.SET_NULL, null=True, blank=True)


class OrderLine(models.Model):
    order = models.ForeignKey(to="Order", on_delete=models.CASCADE)
    service = models.ForeignKey(to="Service", on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField()
