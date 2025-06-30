from django.urls import path
from api import views

app_name = "api"

urlpatterns = [
    path("first/events/", views.GetCurrentFirstEventsAPIView.as_view()),
    path("second/events/", views.GetCurrentSecondEventsAPIView.as_view()),
    path("third/events/", views.GetCurrentThirdEventsAPIView.as_view()),
    path("rates/", views.GetRatesMoneyView.as_view()),
    path("weather/", views.GetWeatherView.as_view()),
]
