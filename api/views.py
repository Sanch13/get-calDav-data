import datetime

import requests.exceptions
import urllib3.exceptions

from django.conf import settings
from django.http import Http404, JsonResponse
from django.core.cache import cache
from django.utils import timezone

from rest_framework import views
from rest_framework.views import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from logs.logging_config import logger
from rooms.services.get_data_from_bitrix import (
    get_bitrix_client,
    get_raw_events,
    get_room_events_json,
    report_bitrix_failure,
    report_bitrix_recovery
)

from rooms.utils import (
    get_caldav_config,
    connect_to_calendar,
    get_sorted_events,
    get_sorted_all_events,
    get_all_events_today_in_json,
    get_rates_today_by_api,
    get_weather_today_by_api,
    get_now_and_midnight, get_sorted_all_events_from_bitrix
)

STALE_THRESHOLD_SECONDS = 5 * 60

def api_room_events(request, room_slug: str):
    room = settings.MEETING_ROOMS.get(room_slug)
    if room is None:
        raise Http404("Комната не найдена")

    client = get_bitrix_client()
    now = datetime.datetime.now().strftime("%Y-%m-%d")
    cache_key = f"room_last_good:{room_slug}"

    try:
        raw_events = get_raw_events(client, room["bitrix_resource_id"], now, now)
        events_room = get_room_events_json(client, raw_events)
        sorted_all_events_today = get_sorted_all_events_from_bitrix(events_room)
        data = get_all_events_today_in_json(sorted_all_events_today)

        cache.set(cache_key, {"data_json": data, "fetched_at": timezone.now().isoformat()}, timeout=None)
        try:
            report_bitrix_recovery()
        except Exception:
            logger.exception("Не удалось обработать recovery-уведомление Bitrix")

    except Exception:
        logger.exception("Bitrix request failed for room %s", room_slug)

        try:
            report_bitrix_failure(room_slug)
        except Exception:
            logger.exception("Не удалось обработать алерт о падении Bitrix")

        cached = cache.get(cache_key)
        if cached:
            fetched_at = datetime.datetime.fromisoformat(cached["fetched_at"])
            age_seconds = (timezone.now() - fetched_at).total_seconds()
            if age_seconds <= STALE_THRESHOLD_SECONDS:
                return JsonResponse({"data_json": cached["data_json"], "main__title": room["name"]}, status=200)

        return JsonResponse({"error": "Ошибка обработки данных."}, status=500)

    return JsonResponse({"data_json": data, "main__title": room["name"]}, status=200)



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
