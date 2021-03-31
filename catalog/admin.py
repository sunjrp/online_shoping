from django.contrib import admin
from .models import Movie,MovieType,MovieTag

admin.site.register(Movie)
admin.site.register(MovieType)
admin.site.register(MovieTag)

# Register your models here.
