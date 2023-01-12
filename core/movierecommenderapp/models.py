from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Show(models.Model):
    show_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    year = models.CharField(max_length=50)
    poster = models.CharField(max_length=500)
    director = models.CharField(max_length=100)
    actors = models.CharField(max_length=500)
    runtime = models.CharField(max_length=50)
    plot = models.CharField(max_length=500)
    box_office = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name


class Rating(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    show_id = models.ForeignKey(Show, on_delete=models.CASCADE)
    rating = models.IntegerField()


# table to connect users and watched shows
class Watched(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    show_id = models.ForeignKey(Show, on_delete=models.CASCADE)
