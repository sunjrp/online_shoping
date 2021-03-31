from django.db import models

# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=20)
    price = models.CharField(max_length=10)
    rating = models.CharField(max_length=5)
    storyline = models.CharField(max_length=200)
    thumbnail = models.ImageField(upload_to='images/')
    release_date = models.DateField()

    @property
    def image_url(self):
        try:
            url = self.thumbnail.url
        except:
            url = ''
        return url


class Type(models.Model):
    has = models.ManyToManyField(Product)
    name = models.CharField(max_length=20)


class User(models.Model):
    username = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    address = models.CharField(max_length=30)
    email = models.CharField(max_length=20)
    password = models.CharField(max_length=20)


class UserLibrary(models.Model):
    own = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    bought_date = models.CharField(max_length=20)
    has = models.ManyToManyField(Product)


class Cart(models.Model):
    own = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    item = models.CharField(max_length=20)
    price = models.CharField(max_length=10)
    have = models.ManyToManyField(Product)