from django.urls import path
from . import views

app_name = "notify"
urlpatterns = [
    path("", view=views.Notifys.as_view(), name="notify"),
]
