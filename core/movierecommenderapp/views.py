from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm
from omdb import OMDBClient
from .models import Show

omdb_api = OMDBClient(apikey="730a97c3")  # can stay for now


def example(request, title):
    movies = omdb_api.get(search=title)
    return render(request, "example.html", {"movies": movies, "title": title})


def index(request):
    return render(request, 'index.html')


def home(request):  # TODO swap with index
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
        return redirect('index')
    else:
        return render(request, 'signUp.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return HttpResponse('Invalid username or password')
    else:
        return render(request, 'login.html')


def logout(request):
    logout(request)
    return redirect('home')


def search():
    return None


def recommend():
    return None


def info():
    return None
