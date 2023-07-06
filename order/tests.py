from django.test import TestCase
from . import models
# Create your tests here.

st = models.Order.objects.all()
print(st.fil)