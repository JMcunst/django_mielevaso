from .views import *
from django.urls import path

app_name = 'guildwar'
urlpatterns = [
    path('defenses/', getDefenseDec, name="defense"),
]