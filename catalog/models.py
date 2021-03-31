from django.db import models
from django.core.files import File
import os
import urllib.request

# Create your models here.


class MovieType(models.Model):
    type = models.CharField(max_length=20)

    def __str__(self):
        return self.type


class MovieTag(models.Model):
    tag = models.CharField(max_length=20)

    def __str__(self):
        return self.tag


class Movie(models.Model):
    name = models.CharField(max_length=50)
    price = models.CharField(max_length=10)
    type = models.ForeignKey(MovieType, on_delete=models.CASCADE, default=None, blank=True, null=True)
    tag = models.ManyToManyField(MovieTag)
    rate = models.CharField(max_length=5)
    storyline = models.CharField(max_length=1000)
    thumbnail_url = models.URLField(default=None)
    thumbnail = models.ImageField(default=None, blank=True, null=True)
    release_date = models.DateField()

    # def get_remote_image(self):
    #     if self.thumbnail_url and not self.thumbnail:
    #         result = urllib.request.urlretrieve(self.thumbnail_url)
    #         self.thumbnail.save(
    #                 os.path.basename(self.thumbnail_url),
    #                 File(open(result[0]))
    #                 )
    #         self.save()

    def __str__(self):
        return self.name
