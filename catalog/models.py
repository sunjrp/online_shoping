from django.db import models

# Create your models here.


class Catalog(models.Model):
    name = models.CharField(max_length=20)
    type = models.CharField(max_length=10)
    price = models.CharField(max_length=10)
    qty = models.CharField(max_length=5)
