from django.db import models

from authentication.models import User

# Create your models here.

class Show(models.Model):
    show = models.CharField(max_length=50, unique=True, null=False)
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



class Rating(models.Model):
    user = models.IntegerField(null=False)
    show = models.CharField(max_length=50, null=False)
    rating = models.IntegerField()


# table to connect users and watched shows
class Watched(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
