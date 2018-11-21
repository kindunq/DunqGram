from django.urls import path
from . import views

app_name = "Notifications"
urlpatterns = [
    path("", view=views.Notifications.as_view(), name="notifications"),
]
