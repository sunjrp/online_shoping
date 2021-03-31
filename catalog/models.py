from django.db import models

# Create your models here.


class MovieType(models.Model):
    type = models.CharField(max_length=10)

    def __str__(self):
        return self.type


class MovieTag(models.Model):
    tag = models.CharField(max_length=10)

    def __str__(self):
        return self.tag


class Movie(models.Model):
    name = models.CharField(max_length=20)
    price = models.CharField(max_length=10)
    mtype = models.ForeignKey(MovieType, on_delete=models.CASCADE)
    mtag = models.ForeignKey(MovieTag, on_delete=models.CASCADE)
    rate = models.CharField(max_length=5)
    storyline = models.CharField(max_length=200)
    thumbnail = models.ImageField(upload_to='images/')
    release_date = models.DateField()

    def __str__(self):
      template = '{0.name} {0.mtype} {0.mtag} {0.price} {0.thumbnail} {0.rate} {0.storyline} {0.release_date}'
      return template.format(self)

    @property
    def imageURL(self):
        try :
            url = self.thumbnail.url
        except:
            url = ''
        return url


