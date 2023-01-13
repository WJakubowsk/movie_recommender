from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, authenticate, get_user_model, logout
from omdb import OMDBClient
from .models import Show, Rating
from django.contrib.auth.decorators import login_required
import pandas as pd
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
        if get_user_model().objects.filter(username=username).exists():
            return render(request, 'signUp.html', {'error': 'Username already exists'})
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
    movie_rating=pd.DataFrame(list(Rating.objects.all().values()))
    print(movie_rating)
    new_user = movie_rating.user_id.unique().shape[0]
    current_user_id = request.user.username

    # if new user not rated any movie, we have to recommend him the best sellers
    if current_user_id > new_user:
        pass

    # create similarity standardized matrix using Pearson's correlation coefficients
    user_ratings = movie_rating.pivot_table(index=['user_id'],columns=['show_id'],values='rating')
    user_ratings_norm = user_ratings.subtract(user_ratings.mean(axis=1), axis = 'rows')
    user_similarity = user_ratings_norm.T.corr()

    # remove the user from similar users list
    user_similarity.drop(index=current_user_id, inplace=True)

    # set user similarity threshold
    user_similarity_threshold = 0.3
    n = 10 #number of similar users 
    # Get top n similar users
    similar_users = user_similarity[user_similarity[current_user_id]>user_similarity_threshold][current_user_id].sort_values(ascending=False)[:n] 

    # pick movies watched by selected user
    current_user_id_watched = user_ratings_norm[user_ratings_norm.index == current_user_id].dropna(axis=1, how='all')

    # select movies that similar users watched. Remove movies that none of the similar users have watched
    similar_user_movies = user_ratings_norm[user_ratings_norm.index.isin(similar_users.index)].dropna(axis=1, how='all')

    # remove films watched by the requested user from recommendations
    similar_user_movies.drop(current_user_id_watched.columns,axis=1, inplace=True, errors='ignore')

    # A dictionary to store item scores
    item_score = {}
    # Loop through items
    for i in similar_user_movies.columns:
        # Get the ratings for movie i
        movie_rating = similar_user_movies[i]
        
        # Create a variable to store the score
        total = 0
        
        # Create a variable to store the number of scores
        count = 0
        
        # Loop through similar users
        for u in similar_users.index:
            # If the movie has rating
            if not pd.isna(movie_rating[u]):
                # Score is the sum of user similarity score multiply by the movie rating
                score = similar_users[u] * movie_rating[u]
            
                # Add the score to the total score for the movie so far
                total += score
                
                # Add 1 to the count
                count += 1
        
        # Get the average score for the item
        item_score[i] = total / count

    # Convert dictionary to pandas dataframe
    item_score = pd.DataFrame(item_score.items(), columns=['movie', 'movie_score'])
        
    # Sort the movies by score
    ranked_item_score = item_score.sort_values(by='movie_score', ascending=False)

    # get recommendations
    n_recommendations = 10 # to set dynamically for user
    movie_list = ranked_item_score['movie'][:n_recommendations]
    context = {'movie_list': movie_list}
    
    return render(request, 'recommend.html')


@login_required(login_url='login')
def info(request):
    # TODO
    return render(request, 'userInfo.html')


def about(request):
    return render(request, 'about.html')
