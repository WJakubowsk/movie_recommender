from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, authenticate, get_user_model, logout
from omdb import OMDBClient
from .models import Show

omdb_api = OMDBClient(apikey="730a97c3")  # can stay for now


def example(request, title):
    movies = omdb_api.get(search=title)
    return render(request, "example.html", {"movies": movies, "title": title})


def index(request):
    return render(request, 'index.html')


def home(request):
    movies = Show.objects.all()
    return render(request, 'home.html', {'movies': movies})


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


def search():
    return None


def recommend():
    return None


def info():
    return None
