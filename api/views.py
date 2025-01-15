from django.conf import settings

from rest_framework import views
from rest_framework.views import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from logs.logging_config import logger

from rooms.utils import (
    get_caldav_config,
    connect_to_calendar,
    get_sorted_events,
    get_sorted_all_events,
    get_all_events_today_in_json,
    get_rates_today_by_api,
    get_weather_today_by_api,
    get_now_and_midnight
)


class GetCurrentFirstEventsAPIView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            now, midnight = get_now_and_midnight()
            events_today = connect_to_calendar(**get_caldav_config(
                url=settings.CALDAV_FIRST_FLOOR_PUBLIC,
                username=None,
                password=None,
            )).date_search(start=now, end=midnight)
        except Exception as e:
            logger.error(f"Ошибка при получении данных с сервера: {e}", exc_info=True)
            return Response(data={"error": f"{e}"},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)

        try:
            sorted_events_today = get_sorted_events(events_today)
            sorted_all_events_today = get_sorted_all_events(sorted_events_today)
            data = get_all_events_today_in_json(sorted_all_events_today)
        except Exception as e:
            logger.error(f"Ошибка при обработке событий: {e}", exc_info=True)
            return Response(data={"error": f"{e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data={"data_json": data, "main__title": "Переговорная 1 этаж"},
                        status=status.HTTP_200_OK)


class GetCurrentThirdEventsAPIView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            now, midnight = get_now_and_midnight()
            events_today = connect_to_calendar(**get_caldav_config(
                url=settings.CALDAV_THIRD_FLOOR_PUBLIC,
                username=None,
                password=None,
            )).date_search(start=now, end=midnight)
        except Exception as e:
            logger.error(f"Ошибка при получении данных с сервера: {e}", exc_info=True)
            return Response(data={"error": f"{e}"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        try:
            sorted_events_today = get_sorted_events(events_today)
            sorted_all_events_today = get_sorted_all_events(sorted_events_today)
            data = get_all_events_today_in_json(sorted_all_events_today)
        except Exception as e:
            logger.error(f"Ошибка при получении данных с сервера: {e}", exc_info=True)
            return Response(data={"error": f"{e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data={"data_json": data, "main__title": "Переговорная 3 этаж"},
                        status=status.HTTP_200_OK)


class GetRatesMoneyView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            rates_today: dict = get_rates_today_by_api()
        except Exception as e:
            logger.error(f"Ошибка при получении данных с сервера курсов валют: {e}", exc_info=True)
            return Response(data={"error": f"{e}"},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response(data=rates_today,
                        status=status.HTTP_200_OK)


class GetWeatherView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            weather_today: dict = get_weather_today_by_api(
                api_key_weather=settings.API_KEY_WEATHER,
                location="Minsk"
            )
        except Exception as e:
            logger.error(f"Ошибка при получении данных с сервера погоды: {e}", exc_info=True)
            return Response(data={"error": f"{e}"},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)

        weather_today = {
            "tempC": weather_today["current"]["temp_c"],
            "icon": weather_today["current"]["condition"]["icon"],
        }

        return Response(data=weather_today,
                        status=status.HTTP_200_OK)
