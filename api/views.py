from datetime import datetime

from django.conf import settings

from rest_framework import views
from rest_framework.views import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from api.serializers import GetDataFromFirstFloorSerializer

from rooms.models.models import FirstRoom

from rooms.utils import (
    get_caldav_config,
    connect_to_calendar,
    get_sorted_events,
    get_sorted_all_events,
    generate_hash,
    get_all_events_today_in_json,
    get_rates_today_by_api,
    get_weather_today_by_api
)


class GetCurrentEventsAPIView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        print("API")

        # Попытка получения данных с сервера
        # try:
        #
        #     events_today = connect_to_calendar(**get_caldav_config(
        #         url=settings.CALDAV_URL,
        #         username=settings.CALDAV_USERNAME,
        #         password=settings.CALDAV_PASSWORD,
        #     )).date_search(start=datetime.now())
        # except Exception as e:
        #     print(f"Ошибка при получении данных с сервера: {e}")
        #     return Response(data={"error": f"{e}"},
        #                     status=status.HTTP_503_SERVICE_UNAVAILABLE)
        #
        # sorted_events_today = get_sorted_events(events_today)
        # sorted_all_events_today = get_sorted_all_events(sorted_events_today)
        # hash_value = generate_hash(sorted_all_events_today)
        #
        # try:
        #     if not FirstRoom.objects.filter(hash_value=hash_value).exists():
        #         print("API - СОЗДАЮ НОВУЮ ЗАПИСЬ в БД")
        #         all_events_today_json = get_all_events_today_in_json(sorted_all_events_today)
        #         serializer = GetDataFromFirstFloorSerializer(data={
        #             "hash_value": hash_value,
        #             "data_json": all_events_today_json,
        #         })
        #         if serializer.is_valid(raise_exception=True):
        #             serializer.save()
        #
        #     instance = FirstRoom.objects.get(hash_value=hash_value)
        # except FirstRoom.DoesNotExist:
        #     return Response(data={"error": "Object not found"},
        #                     status=status.HTTP_404_NOT_FOUND)
        #
        # serializer = GetDataFromFirstFloorSerializer(instance)
        data = {'hash_value': '56344e5782b5c2207c8067230179d78647a0efe2e36b124c4af1c53adb7bc56f',
                'data_json': '[{"end": "2024-11-10T11:29:00+03:00", "start": "2024-11-10T10:29:00+03:00", "status": "reserved", "summary": "xcvbnxfgh"}, {"end": "2024-11-11T00:00:00+03:00", "start": "2024-11-10T11:29:00+03:00", "status": "free", "summary": "\\u0421\\u0412\\u041e\\u0411\\u041e\\u0414\\u041d\\u041e"}]'}
        return Response(data=data,
                        status=status.HTTP_200_OK)


class GetRatesMoneyView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            rates_today: dict = get_rates_today_by_api()
        except Exception as e:
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
            return Response(data={"error": f"{e}"},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)

        weather_today = {
            "tempC": weather_today["current"]["temp_c"],
            "icon": weather_today["current"]["condition"]["icon"],
        }
        print(weather_today)

        return Response(data=weather_today,
                        status=status.HTTP_200_OK)
