from django.contrib import admin
from .models import Show, Rating, Watched, User

admin.site.register(Show)
admin.site.register(User)
admin.site.register(Rating)
admin.site.register(Watched)
# user: admin
# pass: admin
