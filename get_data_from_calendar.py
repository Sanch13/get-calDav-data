import os
import json
import locale

from icalendar import Calendar
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


def connect_to_calendar(url, username, password):
    """
    Подключается к календарю с использованием DAVClient и возвращает объект календаря.
    """
    try:
        with caldav.DAVClient(url=url, username=username, password=password) as client:
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
    # print(credentials)
    print(my_calendar)
    # for event in my_calendar.events():
    #     raw_data = event.data
    #     print(type(raw_data))
    #     print("----------")
        # calendar = Calendar.from_ical(raw_data)
        # for component in calendar.walk('VEVENT'):
        #     print(component)

    now, _ = get_now_and_midnight()
    midnight = (now + timedelta(days=5)).replace(hour=23, minute=59, second=59, microsecond=0)

    print(f"{now} ---- {midnight}")
    # events_today = my_calendar.search(start=now, end=midnight)
    events_today = my_calendar.date_search(start=now, end=midnight)
    # print(f"events_today {len(events_today)} {events_today}")
    # for event in events_today:
    #     raw_data = event.data
    #     calendar = Calendar.from_ical(raw_data)
    #     for component in calendar.walk('VEVENT'):
    #         print("-------------")
            # print("Название события:", component.get("SUMMARY").to_ical().decode("utf-8"))
            # print("Начало:", component.get("DTSTART").dt)
            # print("Конец:", component.get("DTEND").dt)

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
