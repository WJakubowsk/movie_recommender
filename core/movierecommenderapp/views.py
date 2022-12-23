from django.shortcuts import render
from django.http import HttpResponse
# import imdbpie

# imdb = imdbpie.Imdb(apikey='k_8j5')


def say_hello(request):
    return render(request, 'hello.html')


def search(request):
    # movies = imdb.search_for_title('Matrix')
    movies = ['Matrix', 'The Matrix', 'The Matrix Reloaded', 'The Matrix Revolutions']
    return render(request, 'search.html', {'movies': movies})
