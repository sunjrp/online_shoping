from django.db import models

# Create your models here.


class MovieType(models.Model):
    type = models.CharField(max_length=5)



class MovieTag(models.Model):
    tag = models.CharField(max_length=10)


class Movie(models.Model):
    name = models.CharField(max_length=20)
    price = models.CharField(max_length=10)
    type = models.ForeignKey(MovieType, on_delete=models.CASCADE)
    tag = models.ForeignKey(MovieTag, on_delete=models.CASCADE)
    rate = models.CharField(max_length=5)
    storyline = models.CharField(max_length=200)
    thumbnail = models.ImageField()
    release_date = models.DateField()

    def __str__(self):
        return self.name, self.price, self.rate

