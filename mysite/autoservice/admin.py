from django.contrib import admin
from .models import Service, Car, Order, OrderLine

class OrderLineInLine(admin.TabularInline):
    model = OrderLine
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['car', 'date']
    inlines = [OrderLineInLine]

class CarAdmin(admin.ModelAdmin):
    list_display = ['make', 'model', 'license_plate', 'vin_code', 'client_name']
    list_filter = ['client_name', 'make', 'model']

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']

admin.site.register(Service, ServiceAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine)
