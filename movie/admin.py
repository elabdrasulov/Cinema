from django.contrib import admin

from .models import Category, Movie, Rating, Like, Comment, Favorite

admin.site.register(Category)
admin.site.register(Movie)
admin.site.register(Rating)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Favorite)