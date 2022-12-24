from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.say_hello, name='hello'),
    path('search/', views.search),
    path('omdb/<str:title>/', views.omdb_search)
]
