from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, authenticate, get_user_model, logout
from omdb import OMDBClient
from .models import Show
from django.contrib.auth.decorators import login_required
import requests

omdb_api = OMDBClient(apikey="730a97c3")
api_url = 'http://www.omdbapi.com/?apikey=730a97c3'


def example(request, title):
    movies = omdb_api.get(search=title)
    return render(request, "example.html", {"movies": movies, "title": title})


def index(request):
    if request.user.is_authenticated:
        return redirect('home')

    movies = Show.objects.all()  # example shows to display
    movies = list(movies[:10])
    return render(request, 'index.html', {'movies': movies})


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        user = get_user_model().objects.create_user(username=username, email=email, password=password,
                                                    first_name=firstname, last_name=lastname)
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'signUp.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('index')


def save_movie(title):
    if Show.objects.filter(title=title).exists():
        return Show.objects.get(title=title)

    # search for movies with the given title
    response = requests.get(api_url + '&t=' + title)
    if response.json()['Response'] != 'True':
        raise ValueError('Server error')
    # add to DB
    movie = Show(show_id=response.json()['imdbID'], title=response.json()['Title'], year=response.json()['Year'],
                 category=response.json()['Genre'],
                 poster=response.json()['Poster'], director=response.json()['Director'],
                 actors=response.json()['Actors'], runtime=response.json()['Runtime'],
                 plot=response.json()['Plot'], box_office=response.json()['BoxOffice'])
    Show.save(movie)
    return movie


def search_with_api(request):
    query = request.GET.get('q')
    movies = list(omdb_api.get(search=query))
    if movies == None or len(movies) == 0:
        return render(request, 'home.html', {'error': 'No results found'})
    return render(request, "api_results.html", {"movies": movies, "query": query})


def search(request):
    query = request.GET.get('q')
    results = Show.objects.filter(title__contains=query)
    results = list(results)
    if results == None or len(results) == 0:
        # search_for_movies(title) # TODO
        return render(request, 'home.html', {'error': 'No results found'})

    return render(request, 'search_results.html', {'results': results,
                                                   'query': query})


def movie_detail(request, title):
    try:
        movie = save_movie(title)
    except ValueError:
        return HttpResponse('Server error')
    return render(request, 'movie_detail.html', {'movie': movie})


@login_required(login_url='login')
def recommend(request):
    '''
    TODO: implement with existing trained model, or train a new model based on user's ratings
    for now just return a list of movies
    '''
    return None


@login_required(login_url='login')
def info(request):
    # TODO
    return render(request, 'userInfo.html')


def about(request):
    return render(request, 'about.html')
