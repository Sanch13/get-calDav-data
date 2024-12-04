import hashlib
import json
from datetime import datetime, timezone, timedelta

import requests

import caldav
from icalendar import Calendar


def get_caldav_config(url, username, password) -> dict:
    """Возвращает словарь с данными для подключения к серверу по протоколу CalDAV."""
    return {
        "url": url,
        "username": username,
        "password": password,
    }


def connect_to_calendar(url, username, password):
    """
    Подключается к серверному календарю с использованием DAVClient и возвращает объект календаря.
    """
    headers = {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
    }
    try:
        with caldav.DAVClient(url=url,
                              username=username,
                              password=password,
                              headers=headers
                              ) as client:
            my_calendar = client.calendar(url=url)
            return my_calendar
    except Exception as e:
        print(f"Ошибка подключения к календарю: {e}")
        return None


def get_organizer_sent_by(component):
    """Получить организатора мероприятия"""
    if 'ORGANIZER' in component:
        organizer = component.get('ORGANIZER').params.get('SENT-BY')  # Извлекаем параметр SENT-BY
        return organizer.split(":")[-1]


def get_attendees_full_names(component):
    """Возвращает имена и фамилии участников мероприятия"""
    attendees_names = []
    if 'ATTENDEE' in component:
        attendees = component.get('ATTENDEE')
        if isinstance(attendees, list):
            for attendee in attendees:
                cn = attendee.params.get('CN', "No Name")  # Извлекаем параметр CN (имя и фамилия)
                if cn:
                    attendees_names.append(cn)
        else:
            attendees_names.append(component.get('ATTENDEE').params.get('CN', "No Name"))

    return attendees_names


def get_summary(component) -> str:
    """Возвращает наименование события"""
    return component.get('SUMMARY').to_ical().decode("utf-8") if 'SUMMARY' in component else ''


def get_location(component) -> str:
    """Возвращает место проведения события"""
    return component.get("LOCATION") if 'LOCATION' in component else ''


def get_start_time(component) -> str:
    """Возвращает время начала события"""
    return component.get('DTSTART').dt


def get_end_time(component) -> str:
    """Возвращает время окончания события"""
    return component.get("DTEND").dt


def get_category(component) -> str:
    """Возвращает категорию события"""
    return component.get("CATEGORY") if 'CATEGORY' in component else ''


def get_description(component) -> str:
    """Возвращает описание события"""
    return component.get("DESCRIPTION") if 'DESCRIPTION' in component else ''


def get_sorted_events(events) -> list:
    """Возвращает все отсортированные события календаря по времени"""
    all_events = []
    try:
        for event in events:
            raw_data = event.data
            calendar = Calendar.from_ical(raw_data)
            for component in calendar.walk('VEVENT'):
                item = {
                    "summary": get_summary(component) or "",
                    "start": get_start_time(component) or "",
                    "end": get_end_time(component) or "",
                    "status": "reserved"
                    # "location": get_location(component) or "",
                    # "category": get_category(component) or "",
                    # "description": get_description(component) or "",  #
                    # "members": get_attendees_full_names(component) or "",  # Участники
                    # "organizer": get_organizer_sent_by(component) or "",  # Организатор
                }

                all_events.append(item)

        sorted_all_events = sorted(all_events, key=lambda x: x.get("start"))
        return sorted_all_events

    except Exception as e:
        print(f"Ошибка разбора icalendar: {e}")
        return []


def get_now_and_midnight():
    now = datetime.now()
    midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    return now, midnight


def get_sorted_all_events(events):
    """Возвращает все отсортированные события текущего дня."""

    time_now = datetime.now(timezone(timedelta(hours=3)))
    midnight = time_now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)

    all_events_cur_day = []
    for event in events:
        start_time = event.get("start", midnight)
        end_time = event.get("end", midnight)

        if start_time < midnight and end_time > time_now:
            if time_now < start_time:
                all_events_cur_day.append({
                    "summary": "СВОБОДНО",
                    "start": time_now.isoformat(),
                    "end": start_time.isoformat(),
                    "status": "free"
                })

            all_events_cur_day.append({
                "summary": event.get("summary"),
                "start": start_time.isoformat(),
                "end": end_time.isoformat(),
                "status": event.get("status")
            })

            time_now = max(time_now, end_time)

    if time_now < midnight:
        all_events_cur_day.append({
            "summary": "СВОБОДНО",
            "start": time_now.isoformat(),
            "end": midnight.isoformat(),
            "status": "free"
        })

    return all_events_cur_day


def get_all_events_today_in_json(events):
    return json.dumps(events, sort_keys=True)


def generate_hash(data: list) -> str:
    """
    Генерирует SHA-256 хэш для строки.

    :param data: Строка-объект.
    :return: Хэш в шестнадцатеричном формате.
    """
    if len(data) == 1 and data[0]["status"] == 'free':
        data[0]["start"] = "start"
    else:
        if data[0]["status"] == 'free':
            data[0]["start"] = "start"

    str_bytes = str(data).encode('utf-8')
    return hashlib.sha256(str_bytes).hexdigest()


def is_all_time_free_today(events: list) -> bool:
    """
    Возвращает True если нет никахих событий на текущий день

    :param events: Список событий календаря
    :return: Булевое значение
    """
    return len(events) == 1 and events[0]["status"] == 'free'


def get_rates_today_by_api() -> dict:
    """
    Возвращает словарь курсов USD, EUR, RUB, CNY.
    """
    api_url = 'https://api.nbrb.by/exrates/rates/'
    curses = {
        "USD": f"{api_url}USD?parammode=2",
        "EUR": f"{api_url}EUR?parammode=2",
        "RUB": f"{api_url}RUB?parammode=2",
        "CNY": f"{api_url}CNY?parammode=2"
    }

    rates_today = {}

    for key, url_api in curses.items():
        try:
            response = requests.get(url=url_api)
            if response.status_code == 200:
                data = response.json()
                rates_today[key] = f"{data['Cur_OfficialRate']}"
            else:
                print(f"Ошибка: для {key} сервер вернул код {response.status_code}")
        except requests.RequestException as e:
            print(f"Не удалось получить данные для {key}: {e}")

    return rates_today


def get_weather_today_by_api(api_key_weather, location) -> dict:
    URL_WEATHER: str = "https://api.weatherapi.com/v1/current.json"
    params = {
        "key": api_key_weather,
        "q": location,
        "lang": "ru"
    }
    try:
        response = requests.get(url=URL_WEATHER, params=params)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Ошибка: сервер вернул код {response.status_code}")
    except requests.RequestException as e:
        print(f"Не удалось получить данные. Ошибка: {e}")
