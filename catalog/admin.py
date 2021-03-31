from django.contrib import admin
from .models import *

admin.site.register(Product)
admin.site.register(Genre)
admin.site.register(User)
admin.site.register(UserLibrary)
admin.site.register(Cart)


# Register your models here.
