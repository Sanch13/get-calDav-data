import os
import json
import locale

import caldav

from dotenv import load_dotenv

from datetime import datetime, timedelta

# from rooms.utils import (
#     connect_to_calendar,
# )

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
        password=credentials.get("password"),
        ssl_verify_cert=False) as client:

    my_calendar = client.calendar(url=credentials.get("url"))

# <class 'caldav.objects.Calendar'>
# all_events_now = connect_to_calendar(
#     credentials.get("url"),
#     credentials.get("username"),
#     credentials.get("password"),
#     ssl_verify_cert=False
# ).date_search(start=date_now, end=None)

if __name__ == '__main__':
    print()
    print(my_calendar)
    print(my_calendar.date_search(start=date_now, end=None, verify_expand=False))

    now = datetime.today()
    midhigth = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    print(now)
    print(midhigth)

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
    #           event["summary"])
