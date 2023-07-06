from django.contrib import admin
from .models import FirstOrder, SecondOrder, Order

# Register your models here.

admin.site.register(FirstOrder)
admin.site.register(SecondOrder)
