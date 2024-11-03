from django.urls import path
from api import views

app_name = "api"

urlpatterns = [
    path("first/events/", views.GetCurrentEventsAPIView.as_view()),
]
