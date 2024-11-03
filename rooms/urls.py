from django.urls import path
from rooms import views

app_name = "rooms"

urlpatterns = [
    path("first/", views.TheFirstConferenceView.as_view()),
    path("third/", views.TheThirdConferenceView.as_view())
]
