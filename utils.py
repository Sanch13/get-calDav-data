import json
import os
from datetime import datetime, timezone, timedelta

from dotenv import load_dotenv

import caldav
from icalendar import Calendar


def get_caldav_config() -> dict:
    """Возвращает словарь с данными для подключения к серверу CalDAV."""
    load_dotenv()  # Загрузка переменных из .env
    return {
        "url": os.getenv("CALDAV_URL"),
        "username": os.getenv("CALDAV_USERNAME"),
        "password": os.getenv("CALDAV_PASSWORD"),
    }


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
    return component.get('SUMMARY') if 'SUMMARY' in component else ''


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


def get_sorted_all_events(events) -> list:
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


def get_all_events_in_json(events):
    """Возвращает все события текущего дня в json"""

    time_now = datetime.now(timezone(timedelta(hours=3)))
    midnight = (time_now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)

    all_events_cur_day = []

    for event in events:
        start_time = event.get("start", midnight)

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
            "end": event.get("end").isoformat(),
            "status": event.get("status")
        })

        time_now = event.get("end")

    if time_now < midnight:
        all_events_cur_day.append({
            "summary": "СВОБОДНО",
            "start": time_now.isoformat(),
            "end": midnight.isoformat(),
            "status": "free"
        })

    return json.dumps(all_events_cur_day, ensure_ascii=False, indent=4)

