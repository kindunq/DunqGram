from django.urls import path
from . import views

app_name = "Feed"
urlpatterns = [
    path("", view=views.Feed.as_view(), name="feed"),
]
