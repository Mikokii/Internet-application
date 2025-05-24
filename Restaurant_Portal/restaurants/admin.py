from django.contrib import admin
from .models import CuisineType, Restaurant, Comment

admin.site.register(Restaurant)
admin.site.register(Comment)
admin.site.register(CuisineType)  # Assuming CuisineType is also defined in models.py