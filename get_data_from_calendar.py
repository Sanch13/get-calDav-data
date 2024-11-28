import os
import json
import locale

import caldav
from dotenv import load_dotenv

from datetime import datetime, timedelta, timezone

from rooms.utils import (
    connect_to_calendar,
    get_sorted_events,
    get_sorted_all_events,
)

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')  # Установка русской локали


def get_caldav_config_miran_by() -> dict:
    """Возвращает словарь с данными для подключения к серверу CalDAV."""

    load_dotenv()  # Загрузка переменных из .env

    return {
        "url": os.getenv("CALDAV_URL"),
        "username": os.getenv("CALDAV_USERNAME"),
        "password": os.getenv("CALDAV_PASSWORD"),
    }


def get_caldav_config_miran_bel_com() -> dict:
    """Возвращает словарь с данными для подключения к серверу CalDAV."""

    load_dotenv()  # Загрузка переменных из .env

    return {
        "url": os.getenv("CALDAV_FIRST_FLOOR_URL"),
        "username": os.getenv("CALDAV_FIRST_FLOOR_USERNAME"),
        "password": os.getenv("CALDAV_FIRST_FLOOR_PASSWORD"),
    }


def get_now_and_midnight():
    now = datetime.now()
    midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    return now, midnight


def connect_to_calendar(url, username, password, ssl_verify_cert=True):
    """
    Подключается к календарю с использованием DAVClient и возвращает объект календаря.
    """
    try:
        with caldav.DAVClient(url=url, username=username, password=password, ssl_verify_cert=True) as client:
            my_calendar = client.calendar(url=url)
            return my_calendar
    except Exception as e:
        print(f"Ошибка подключения к календарю: {e}")
        return None


# credentials = get_caldav_config_miran_by()       # mail.miran.by
credentials = get_caldav_config_miran_bel_com()  # mail.miran-bel.com

date_now = datetime.now()

with caldav.DAVClient(
        url=credentials.get("url"),
        username=credentials.get("username"),
        password=credentials.get("password")) as client:

    my_calendar = client.calendar(url=credentials.get("url"))

# <class 'caldav.objects.Calendar'>
# all_events_now = connect_to_calendar(
#     credentials.get("url"),
#     credentials.get("username"),
#     credentials.get("password"),
#     ssl_verify_cert=False
# ).date_search(start=date_now, end=None)

# NOW = datetime.today()
# MIDNIGHT = (NOW + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)


if __name__ == '__main__':
    # now, midnight = get_now_and_midnight()
    # midnight = (now + timedelta(days=1)).replace(hour=23, minute=59, second=59, microsecond=0)
    # Установка временной зоны UTC+3
    tz = timezone(timedelta(hours=3))

    # Начало дня (полночь текущего дня)
    start = datetime.now(tz).replace(hour=0, minute=0, second=0, microsecond=0)

    # Конец дня (полночь следующего дня)
    end = start + timedelta(days=1)

    print(f"Start: {start}, End: {end}")


    print()
    print(my_calendar)
    # print(f"{now} - {midnight}")
    print(f"{start} - {end}")
    events_today = my_calendar.date_search(start=start, end=end)
    print(f"events_today {len(events_today)} {events_today}")
    # for event in events_today:
    #     print({event.get("start"), event.get("summary")})

    sorted_events_today = get_sorted_events(events_today)

    print(f"sorted_events_today {len(sorted_events_today)}")
    for event in sorted_events_today:
        print(f'''{event.get("start").strftime('%Y-%m-%d %H:%M')}:{event.get("end").strftime('%Y-%m-%d %H:%M')} {event.get("summary")}''')

    sorted_all_events_today = get_sorted_all_events(sorted_events_today)
    print(f"sorted_all_events_today {len(sorted_all_events_today)} {sorted_all_events_today}")
    for event in sorted_all_events_today:
        print(f'''{event.get("start")}:{event.get("end")} {event.get("summary")}''')

    # now = datetime.today()
    # midhigth = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    # print(now)
    # print(midhigth)

    # print(all_events_now)

    # sorted_events = get_sorted_all_events(all_events_now)
    # all_events_cur_day = get_all_events_in_json(sorted_events)

    # with open("example.json", "w", encoding="utf-8") as file:
    #     file.write(all_events_cur_day)

    # with open("example.json", "r", encoding="utf-8") as file:
    #     all_data = json.loads(file.read())
    #
    # for event in all_data:
    #     print(datetime.fromisoformat(event["start"]).strftime("%H:%M"),
    #           datetime.fromisoformat(event["end"]).strftime("%H:%M"),
    #           event["status"],
    #           event["summary"])cal.



'''
Как избежать кеширования

Если вы подозреваете, что сервер или клиент кеширует ответы, 
есть несколько способов предотвратить кеширование:

Использовать уникальные параметры в URL-запросах: Например, можно добавить временную метку к запросу:

url_with_timestamp = f"{url}?timestamp={datetime.now().timestamp()}"

Это заставит сервер считать запрос уникальным, избегая кеширования.

Добавить заголовки для предотвращения кеширования: Если сервер или клиент поддерживает кеширование, 
можно добавить заголовки для указания, чтобы кеширование не происходило:

headers = {
    'Cache-Control': 'no-cache, no-store, must-revalidate',
    'Pragma': 'no-cache',
    'Expires': '0'
}

# Пример использования с requests:
response = requests.get(url, headers=headers)

Настроить сервер для отключения кеширования: Если вы управляете сервером CalDAV, можно настроить 
его так, чтобы он не кешировал запросы или обновлял данные в реальном времени. Это зависит от 
конфигурации сервера CalDAV.
'''