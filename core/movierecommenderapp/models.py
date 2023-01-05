from django.db import models
# Create your models here.

class Show(models.Model):
    movie_id = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    year = models.CharField(max_length=50)
    Poster = models.CharField(max_length=500)
    Director = models.CharField(max_length=100)
    Actors = models.CharField(max_length=500)
    Runtime = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class User(models.Model): #TODO change to auth.user
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    rating = models.IntegerField()

# table to connect users and watched shows
class Watched(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)

#uzytkowanik podaje dane,