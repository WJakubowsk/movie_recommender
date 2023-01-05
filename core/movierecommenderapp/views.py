from django.shortcuts import render
from omdb import OMDBClient

omdb_api = OMDBClient(apikey="730a97c3")


def example(request, title):
    movies = omdb_api.get(search=title)
    return render(request, "omdb_search.html", {"movies": movies, "title": title})


def home(request):
    return render(request, 'home.html')


def signup():
    return None


def login():
    return None


def logout():
    return None


def search():
    return None


def recommend():
    return None


def info():
    return None