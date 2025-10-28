from django.db import models


class Service(models.Model):
    name = models.CharField()
    price = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Paslauga"
        verbose_name_plural = "Paslaugos"

class Car(models.Model):
    make = models.CharField()
    model = models.CharField()
    license_plate = models.CharField()
    vin_code = models.CharField()
    client_name = models.CharField()

    def __str__(self):
        return f"{self.make} {self.model}"

    class Meta:
        verbose_name = "Automobilis"
        verbose_name_plural = "Automobiliai"


class Order(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    car = models.ForeignKey(to="Car", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.car} - {self.date}"

    class Meta:
        verbose_name = "Užsakymas"
        verbose_name_plural = "Užsakymai"

    def total(self):
        result = 0
        for line in self.lines.all():
            result += line.line_sum()
        return result



class OrderLine(models.Model):
    order = models.ForeignKey(to="Order", on_delete=models.CASCADE, related_name="lines")
    service = models.ForeignKey(to="Service", on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.service} ({self.service.price}) - {self.quantity}"

    def line_sum(self):
        return self.service.price * self.quantity

    line_sum.short_description = "Suma"

    class Meta:
        verbose_name = "Eilutė"
        verbose_name_plural = "Eilutės"
