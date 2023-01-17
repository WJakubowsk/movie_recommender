from django.contrib import admin
from .models import Show, Rating, Watched, User
from django.contrib.auth import get_user_model

admin.site.register(Show)
admin.site.register(Rating)
admin.site.register(Watched)
# user: admin
# pass: admin
