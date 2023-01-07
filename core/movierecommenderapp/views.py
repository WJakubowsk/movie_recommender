from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, authenticate, get_user_model, logout
from omdb import OMDBClient
from .models import Show

omdb_api = OMDBClient(apikey="730a97c3")  # can stay for now


def example(request, title):
    movies = omdb_api.get(search=title)
    return render(request, "example.html", {"movies": movies, "title": title})


def index(request):
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
            return HttpResponse('Invalid username or password')
    else:
        return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('index')


def search(request):
    query = request.GET.get('q')
    results = Show.objects.filter(title__contains=query)
    results = list(results)
    if results == None or len(results) == 0:
        return render(request, 'home.html', {'error': 'No results found'})

    return render(request, 'search_results.html', {'results': results,
                                                   'query': query})


def recommend(request):
    '''
    TODO: implement with existing trained model, or train a new model based on user's ratings
    for now just return a list of movies
    '''
    return None


def info(request):
    # TODO
    return None
