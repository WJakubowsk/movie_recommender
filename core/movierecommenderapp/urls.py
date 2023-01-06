from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout, name='logout'),
    path('search/', views.search, name='search'),
    path('recommend/', views.recommend, name='recommend'),
    path('info', views.info, name='info'),
    path('omdb/<str:title>/', views.example, name='example'),
]
