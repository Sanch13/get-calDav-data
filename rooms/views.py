import hashlib
import json
from datetime import datetime, timedelta

from django.shortcuts import render, get_object_or_404

from rest_framework import views
from rest_framework.permissions import AllowAny

from rooms.utils import (
    get_caldav_config,
    generate_hash,
    connect_to_calendar,
    get_sorted_events,
    get_sorted_all_events,
    get_all_events_today_in_json,
    is_all_time_free_today
)
from rooms.models.models import FirstRoom


class TheFirstConferenceView(views.APIView):
    permission_classes = [AllowAny]

    # сделать POST запрос с hash.
    # если крайняя запись hash в БД не равна текущей hash с фронта то было обновление данных в БД
    # вернуть ответ на фронт что есть обновление

    def get(self, request):
        # вынести логику запроса (опроса по тайм ауту)  к почтовому серверу в celery
        credentials = get_caldav_config()
        date_today = datetime.now()
        events_today = connect_to_calendar(**credentials).date_search(start=date_today)

        sorted_events_today = get_sorted_events(events_today)
        sorted_all_events_today = get_sorted_all_events(sorted_events_today)
        if is_all_time_free_today(sorted_all_events_today):
            # если количество ивентов 1 и статус free то берем данные из redis
            # или генерируем данные в json начало и конца свободного времени
            print("ТОЛЬКО СВОБОДНОЕ ВЕРМЯ")

        print("Количество ивентов на сегодня", len(sorted_all_events_today))

        # в других случаях генерируем hash и проверям в БД есть ли такие ивенты
        hash_value = generate_hash(sorted_all_events_today)

        print("Хеш ивентов", hash_value)

        all_events_today_json = get_all_events_today_in_json(sorted_all_events_today)

        if not FirstRoom.objects.filter(hash_value=hash_value).exists():
            print("СОЗДАЮ НОВУЮ ЗАПИСЬ в БД")
            FirstRoom.objects.create(hash_value=hash_value,
                                     data_json=all_events_today_json)
        # вынести логику запроса (опроса по тайм ауту)  к почтовому серверу в celery


        # тут будет запрос только на последнюю запись (обновление данных на фронте) из БД
        # сделать проверку если евентов нет достать запись с
        # ХРАНИТЬ ТОЛЬКО ИВЕНТЫ !!!
        context = {
            "data": get_object_or_404(FirstRoom, hash_value=hash_value).data_json
        }

        return render(request=request,
                      template_name="rooms/index_old.html",
                      context=context)
