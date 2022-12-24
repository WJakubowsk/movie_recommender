from django.shortcuts import render
from django.http import HttpResponse
from omdb import OMDBClient

moviesDB = OMDBClient(apikey="730a97c3")


def say_hello(request):
    return render(request, 'hello.html')


def search(request):
    movies = ['Matrix', 'The Matrix',
              'The Matrix Reloaded', 'The Matrix Revolutions']
    return render(request, 'search.html', {'movies': movies})


def omdb_search(request, title):
    movies = moviesDB.get(search=title)
    return render(request, "omdb_search.html", {"movies": movies ,"title": title})
