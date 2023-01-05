from django.shortcuts import render
from omdb import OMDBClient

omdb_api = OMDBClient(apikey="730a97c3")


def say_hello(request):
    return render(request, 'hello.html')

def omdb_search(request, title):
    movies = omdb_api.get(search=title)
    return render(request, "omdb_search.html", {"movies": movies, "title": title})


def home(request):
    return render(request, 'home.html')