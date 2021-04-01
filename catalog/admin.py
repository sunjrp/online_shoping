from django.contrib import admin
from .models import *


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'price')


admin.site.register(Product, ProductAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(User)
admin.site.register(UserLibrary)
admin.site.register(Cart)


# Register your models here.
