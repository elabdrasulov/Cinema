from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


GENRE  = [
    ('ACTION', 'Action'),
    ('FANTASY', 'Fantasy'),
    ('HORROR', 'Horror'),
    ('ADVENTURE', 'Adventure'),
    ('COMEDY', 'Comedy'),
]

class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Movie(models.Model):
    categories = models.ManyToManyField(Category, related_name='movies', blank=True)
    title = models.CharField(max_length=100)
    genre = models.CharField(choices=GENRE, max_length=100, blank=True)
    year = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='movies', blank=True, null=True)
    director = models.CharField(max_length=100, blank=True)
    actors = models.CharField(max_length=10000, blank=True)
    desc = models.TextField(max_length=10000, blank=True)

    @property
    def average_rating(self):
        ratings = [rating.value for rating in self.ratings.all()]
        if ratings:
            return sum(ratings) / len(ratings)
        else:
            return 0 

    def __str__(self):
        return self.title


class Rating(models.Model):
    user = models.ForeignKey(User, related_name='ratings', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='ratings', on_delete=models.CASCADE)
    value = models.IntegerField(choices=[(1,1), (2,2), (3,3), (4,4), (5,5),(6,6), (7,7), (8,8), (9,9), (10,10)])

    def __str__(self):
        return f'{self.user} -> {self.movie}'

class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} -> {self.movie}'


class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='likes', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} -> {self.movie}'

class Favorite(models.Model):
    user = models.ForeignKey(User, related_name='favorites', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='favorites', on_delete=models.CASCADE)
    favorited = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} -> {self.movie}'