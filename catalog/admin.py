from django.contrib import admin

# Register your models here.

from catalog.models import Movie
from catalog.models import MovieTag
from catalog.models import MovieType

admin.site.register(Movie)
admin.site.register(MovieTag)
admin.site.register(MovieType)
