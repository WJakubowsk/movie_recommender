import random
import pandas as pd
import requests
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, HttpResponse, redirect
from omdb import OMDBClient
from .models import Show, Rating, Watched
from django.utils import timezone

omdb_api = OMDBClient(apikey="730a97c3")
api_url = 'http://www.omdbapi.com/?apikey=730a97c3'


def index(request):
    if request.user.is_authenticated:
        return redirect('home')

    movies = Show.objects.all()  # example shows to display
    movies = list(movies[:10])
    return render(request, 'index.html', {'movies': movies})


def home(request):
    movies = Show.objects.all()
    max_range = min(20, len(movies))
    rangee = max(int(request.GET.get('rangee', max_range // 2)), 1)
    movies = random.sample(list(movies), rangee)
    if movies == []:
        return render(request, 'home.html')
    return render(request, 'home.html', {'movies': movies, 'max_range': max_range})


def save_movie_toDB(title):
    if Show.objects.filter(title=title).exists():
        return Show.objects.get(title=title)

    # search for movies with the given title
    response = requests.get(api_url + '&t=' + title)
    if response.json()['Response'] != 'True':
        raise ValueError('Server error')
    # add to DB
    movie = Show(show=response.json()['imdbID'], title=response.json()['Title'], year=response.json()['Year'],
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


def movie_detail(request, title):
    try:
        movie = save_movie_toDB(title)
    except ValueError:
        return HttpResponse('Server error')
    is_watched = Watched.objects.filter(user=request.user, show=movie).exists()
    return render(request, 'movie_detail.html', {'movie': movie, 'is_watched': is_watched})


@login_required(login_url='login')
def recommend(request):
    movie_rating = pd.DataFrame(list(Rating.objects.all().values()))
    movies = pd.DataFrame(list(Show.objects.all().values()))
    current_user_id = request.user.user
    n_recommendations = 10  # to set dynamically for user
    number_of_rated_movies = 0
    # if new user not rated any movie, we have to recommend him the highest-rated movies
    if current_user_id not in movie_rating.user.unique():
        movie_list = (movie_rating.groupby('show').mean()['rating'] * movie_rating.groupby('show').count()['rating']) \
                         .sort_values(ascending=False) \
                         .reset_index()['show'] \
                         .iloc[:n_recommendations] \
            .astype(int) \
            .to_list()
    else:
        # create similarity standardized matrix using Pearson's correlation coefficients
        user_ratings = movie_rating.pivot_table(index=['user'], columns=['show'], values='rating')
        user_ratings_norm = user_ratings.subtract(user_ratings.mean(axis=1), axis='rows')
        user_similarity = user_ratings_norm.T.corr()

        # get number of ratings given by the user
        number_of_rated_movies = user_ratings.loc[current_user_id].notna().sum()
        # remove the user from similar users list
        user_similarity.drop(index=current_user_id, inplace=True)
        # set user similarity threshold
        user_similarity_threshold = 0.3
        n = 10  # number of similar users
        # Get top n similar users
        similar_users = user_similarity[user_similarity[current_user_id] > user_similarity_threshold][
                            current_user_id].sort_values(ascending=False).iloc[:n]

        # pick movies watched by selected user
        current_user_id_watched = user_ratings_norm[user_ratings_norm.index == current_user_id].dropna(axis=1,
                                                                                                       how='all')

        # select movies that similar users watched. Remove movies that none of the similar users have watched
        similar_user_movies = user_ratings_norm[user_ratings_norm.index.isin(similar_users.index)].dropna(axis=1,
                                                                                                          how='all')

        # remove films watched by the requested user from recommendations
        # bypass for now, to be removed
        similar_user_movies.drop(current_user_id_watched.columns, axis=1, inplace=True, errors='ignore')
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
        movie_list = ranked_item_score['movie'].iloc[:n_recommendations].astype(int).to_list()

    recommendations = movies.loc[movies['id'].isin(movie_list)].to_dict('records')
    context = {'movies': recommendations, 'n_rated_movies': number_of_rated_movies}
    return render(request, 'recommend.html', context)


@login_required(login_url='login')
def info(request):
    user = request.user
    if user.is_authenticated:
        now = timezone.now()
        registration_time = now - user.date_joined
        registration_time = registration_time.days

    user_movies = Watched.objects.filter(user=request.user.user)
    time_watched = [int(movie.show.runtime.split(' ')[0]) for movie in user_movies]
    sum_watched = sum(time_watched)

    return render(request, 'userInfo.html',
                  {'user': user, 'registration_time': registration_time, 'sum_watched': sum_watched})


def about(request):
    return render(request, 'about.html')


@login_required(login_url='login')
def list_view(request):
    user_movies = Watched.objects.filter(user=request.user.user)
    user_movies = [movie.show for movie in user_movies]
    if not Watched.objects.filter(user=request.user).exists():
        return render(request, 'home.html', {'error': 'No movies in your list'})
    return render(request, 'list.html', {'user_movies': list(user_movies)})


def save_movie_watched(request):
    if request.method == 'POST':
        show = request.POST.get('movie')
        user = request.user
        assert Show.objects.filter(title=show).exists()
        if Watched.objects.filter(user=user, show=Show.objects.get(title=show)).exists():
            return render('list.html', {'error': 'Movie already in list'})
        saved_show = Watched(user=user, show=Show.objects.get(title=show))
        saved_show.save()
    return redirect('list')


def remove_movie_watched(request):
    if request.method == 'POST':
        show = request.POST.get('movie')
        user = request.user
        Watched.objects.filter(user=user, show=Show.objects.get(title=show)).delete()
    return redirect('list')
