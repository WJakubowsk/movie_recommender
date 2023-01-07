from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from omdb import OMDBClient
from .models import Show

omdb_api = OMDBClient(apikey="730a97c3") # can stay for now

def example(request, title):
    movies = omdb_api.get(search=title)
    return render(request, "example.html", {"movies": movies, "title": title})


def home(request):
    movies = Show.objects.all()
    return render(request, 'home.html', {'movies': movies})

def signup(request):

    form = UserCreationForm()
    return render(request, 'signUp.html', {'form' : form})

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