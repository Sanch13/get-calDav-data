import requests.exceptions
import urllib3.exceptions

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



        # --- Обработка сетевых и SSL ошибок ---
        except requests.exceptions.SSLError as e:
            # Ошибки, связанные с SSL/сертификатами
            logger.error(f"Ошибка SSL-сертификата при подключении к серверу календаря: {e}",
                         exc_info=True)
            error_msg = "Ошибка SSL-сертификата при подключении к серверу"
            return Response(
                data={"error": error_msg},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        except urllib3.exceptions.SSLError as e:
            # На случай, если используется urllib3 напрямую
            logger.error(f"Ошибка SSL (urllib3) при подключении к серверу календаря: {e}",
                         exc_info=True)
            error_msg = "Ошибка SSL-сертификата при подключении к серверу"
            return Response(
                data={"error": error_msg},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        except requests.exceptions.Timeout:
            logger.error("Таймаут при подключении к серверу календаря", exc_info=True)
            return Response(
                data={"error": "Сервер не отвечает. Попробуйте позже."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        except requests.exceptions.ConnectionError:
            logger.error("Ошибка соединения с почтовым сервером", exc_info=True)
            return Response(
                data={"error": "Ошибка соединения с почтовым сервером."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        except requests.exceptions.RequestException:
            logger.error("Неизвестная ошибка запроса к серверу", exc_info=True)
            return Response(
                data={"error": "Неизвестная ошибка запроса к серверу."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        # --- Конец обработки сетевых ошибок ---

        except Exception as e:
            logger.error(f"Ошибка при получении данных с сервера: {e}", exc_info=True)
            return Response(
                data={"error": "Ошибка на стороне сервера. Попробуйте позже."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        try:
            sorted_events_today = get_sorted_events(events_today)
            print(f"sorted_events_today {sorted_events_today}")
            sorted_all_events_today = get_sorted_all_events(sorted_events_today)
            data = get_all_events_today_in_json(sorted_all_events_today)
        except Exception as e:
            logger.error(f"Ошибка обработки данных.", exc_info=True)
            return Response(data={"error": f"Ошибка обработки данных."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data={"data_json": data, "main__title": "Переговорная 1 этаж"},
                        status=status.HTTP_200_OK)


class GetCurrentSecondEventsAPIView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            now, midnight = get_now_and_midnight()
            events_today = connect_to_calendar(**get_caldav_config(
                url=settings.CALDAV_SECOND_FLOOR_PUBLIC,
                username=None,
                password=None,
            )).date_search(start=now, end=midnight)

        # --- Обработка сетевых и SSL ошибок ---
        except requests.exceptions.SSLError as e:
            # Ошибки, связанные с SSL/сертификатами
            logger.error(f"Ошибка SSL-сертификата при подключении к серверу календаря: {e}",
                         exc_info=True)
            error_msg = "Ошибка SSL-сертификата при подключении к серверу"
            return Response(
                data={"error": error_msg},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        except urllib3.exceptions.SSLError as e:
            # На случай, если используется urllib3 напрямую
            logger.error(f"Ошибка SSL (urllib3) при подключении к серверу календаря: {e}",
                         exc_info=True)
            error_msg = "Ошибка SSL-сертификата при подключении к серверу"
            return Response(
                data={"error": error_msg},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        except requests.exceptions.Timeout:
            logger.error("Таймаут при подключении к серверу календаря", exc_info=True)
            return Response(
                data={"error": "Сервер не отвечает. Попробуйте позже."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        except requests.exceptions.ConnectionError:
            logger.error("Ошибка соединения с почтовым сервером", exc_info=True)
            return Response(
                data={"error": "Ошибка соединения с почтовым сервером."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        except requests.exceptions.RequestException:
            logger.error("Неизвестная ошибка запроса к серверу", exc_info=True)
            return Response(
                data={"error": "Неизвестная ошибка запроса к серверу."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        # --- Конец обработки сетевых ошибок ---

        except Exception as e:
            logger.error(f"Ошибка при получении данных с сервера: {e}", exc_info=True)
            return Response(
                data={"error": "Ошибка на стороне сервера. Попробуйте позже."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        try:
            sorted_events_today = get_sorted_events(events_today)
            sorted_all_events_today = get_sorted_all_events(sorted_events_today)
            data = get_all_events_today_in_json(sorted_all_events_today)
        except Exception as e:
            logger.error(f"Ошибка обработки данных.", exc_info=True)
            return Response(data={"error": f"Ошибка обработки данных."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data={"data_json": data, "main__title": "Переговорная 2 этаж"},
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

        # --- Обработка сетевых и SSL ошибок ---
        except requests.exceptions.SSLError as e:
            # Ошибки, связанные с SSL/сертификатами
            logger.error(f"Ошибка SSL-сертификата при подключении к серверу календаря: {e}",
                         exc_info=True)
            error_msg = "Ошибка SSL-сертификата при подключении к серверу"
            return Response(
                data={"error": error_msg},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        except urllib3.exceptions.SSLError as e:
            # На случай, если используется urllib3 напрямую
            logger.error(f"Ошибка SSL (urllib3) при подключении к серверу календаря: {e}",
                         exc_info=True)
            error_msg = "Ошибка SSL-сертификата при подключении к серверу"
            return Response(
                data={"error": error_msg},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        except requests.exceptions.Timeout:
            logger.error("Таймаут при подключении к серверу календаря", exc_info=True)
            return Response(
                data={"error": "Сервер не отвечает. Попробуйте позже."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        except requests.exceptions.ConnectionError:
            logger.error("Ошибка соединения с почтовым сервером", exc_info=True)
            return Response(
                data={"error": "Ошибка соединения с почтовым сервером."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        except requests.exceptions.RequestException:
            logger.error("Неизвестная ошибка запроса к серверу", exc_info=True)
            return Response(
                data={"error": "Неизвестная ошибка запроса к серверу."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        # --- Конец обработки сетевых ошибок ---

        except Exception as e:
            logger.error(f"Ошибка при получении данных с сервера: {e}", exc_info=True)
            return Response(
                data={"error": "Ошибка на стороне сервера. Попробуйте позже."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        try:
            sorted_events_today = get_sorted_events(events_today)
            sorted_all_events_today = get_sorted_all_events(sorted_events_today)
            data = get_all_events_today_in_json(sorted_all_events_today)
        except Exception as e:
            logger.error(f"Ошибка обработки данных.", exc_info=True)
            return Response(data={"error": f"Ошибка обработки данных."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data={"data_json": data, "main__title": "Переговорная 3 этаж"},
                        status=status.HTTP_200_OK)


class GetCurrentClassRoomEventsAPIView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            now, midnight = get_now_and_midnight()
            events_today = connect_to_calendar(**get_caldav_config(
                url=settings.CALDAV_CLASS_ROOM_PUBLIC,
                username=None,
                password=None,
            )).date_search(start=now, end=midnight)

        # --- Обработка сетевых и SSL ошибок ---
        except requests.exceptions.SSLError as e:
            # Ошибки, связанные с SSL/сертификатами
            logger.error(f"Ошибка SSL-сертификата при подключении к серверу календаря: {e}",
                         exc_info=True)
            error_msg = "Ошибка SSL-сертификата при подключении к серверу"
            return Response(
                data={"error": error_msg},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        except urllib3.exceptions.SSLError as e:
            # На случай, если используется urllib3 напрямую
            logger.error(f"Ошибка SSL (urllib3) при подключении к серверу календаря: {e}",
                         exc_info=True)
            error_msg = "Ошибка SSL-сертификата при подключении к серверу"
            return Response(
                data={"error": error_msg},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        except requests.exceptions.Timeout:
            logger.error("Таймаут при подключении к серверу календаря", exc_info=True)
            return Response(
                data={"error": "Сервер не отвечает. Попробуйте позже."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        except requests.exceptions.ConnectionError:
            logger.error("Ошибка соединения с почтовым сервером", exc_info=True)
            return Response(
                data={"error": "Ошибка соединения с почтовым сервером."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        except requests.exceptions.RequestException:
            logger.error("Неизвестная ошибка запроса к серверу", exc_info=True)
            return Response(
                data={"error": "Неизвестная ошибка запроса к серверу."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        # --- Конец обработки сетевых ошибок ---

        except Exception as e:
            logger.error(f"Ошибка при получении данных с сервера: {e}", exc_info=True)
            return Response(
                data={"error": "Ошибка на стороне сервера. Попробуйте позже."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        # --- Обработка данных ---
        try:
            sorted_events_today = get_sorted_events(events_today)
            sorted_all_events_today = get_sorted_all_events(sorted_events_today)
            data = get_all_events_today_in_json(sorted_all_events_today)
        except Exception as e:
            logger.error(f"Ошибка обработки данных.", exc_info=True)
            return Response(data={"error": f"Ошибка обработки данных."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data={"data_json": data, "main__title": "Учебный центр непрерывного совершенствования"},
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

        if weather_today:
            weather_today = {
                "tempC": weather_today["current"]["temp_c"],
                "icon": weather_today["current"]["condition"]["icon"],
            }
        return Response(data=weather_today,
                        status=status.HTTP_200_OK)
