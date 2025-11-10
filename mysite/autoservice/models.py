from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField
from django.contrib.auth.models import AbstractUser
from PIL import Image

class CustomUser(AbstractUser):
    photo = models.ImageField(upload_to="profile_pics", null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.photo:
            img = Image.open(self.photo.path)
            min_side = min(img.width, img.height)
            left = (img.width - min_side) // 2
            top = (img.height - min_side) // 2
            right = left + min_side
            bottom = top + min_side
            img = img.crop((left, top, right, bottom))
            img = img.resize((300, 300), Image.LANCZOS)
            img.save(self.photo.path)

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
    photo = models.ImageField(upload_to="car_photos", null=True, blank=True)
    description = HTMLField(verbose_name="Description", default="")

    def __str__(self):
        return f"{self.make} {self.model}"

    class Meta:
        verbose_name = "Automobilis"
        verbose_name_plural = "Automobiliai"


class Order(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    car = models.ForeignKey(to="Car", on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('c', "Confirmed"),
        ('i', 'In Progress'),
        ('o', 'Completed'),
        ('c', 'Canceled'),
    )

    status = models.CharField(verbose_name="Būsena", max_length=1, choices=LOAN_STATUS, default="c", blank=True)
    client = models.ForeignKey(to="autoservice.CustomUser", on_delete=models.SET_NULL, null=True, blank=True)
    deadline = models.DateTimeField()

    def is_overdue(self):
        return timezone.now() > self.deadline

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


class OrderComment(models.Model):
    order = models.ForeignKey(to="Order", on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(to="autoservice.CustomUser", on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()


    class Meta:
        verbose_name = "Komentaras"
        verbose_name_plural = "Komentarai"
        ordering = ['-pk']

