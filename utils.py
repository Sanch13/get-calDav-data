import json
import os
from datetime import datetime

from dotenv import load_dotenv

import caldav
from icalendar import Calendar


def get_caldav_config():
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


def get_text_format_datetime(date_obj: datetime) -> str:
    # %d %B %Y # day B Year
    return date_obj.strftime("%H:%M")


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
        for attendee in attendees:
            cn = attendee.params.get('CN', "No Name")  # Извлекаем параметр CN (имя и фамилия)
            if cn:
                attendees_names.append(cn)

    return attendees_names


def get_summary(component) -> str:
    """Возвращает событие мероприятия"""
    return component.get('SUMMARY') if 'SUMMARY' in component else ''


def get_location(component) -> str:
    """Возвращает место проведения"""
    return component.get("LOCATION") if 'LOCATION' in component else ''


def get_start_time(component) -> datetime:
    """Возвращает начало времени проведения"""
    return component.get('DTSTART').dt


def get_end_time(component) -> datetime:
    """Возвращает конец времени проведения"""
    return component.get("DTEND").dt if 'DTEND' in component else ''


def get_category(component) -> str:
    """Возвращает конец времени проведения"""
    return component.get("CATEGORY") if 'CATEGORY' in component else ''


def get_description(component) -> str:
    """Возвращает конец времени проведения"""
    return component.get("DESCRIPTION") if 'DESCRIPTION' in component else ''


def get_all_events_json(all_events):
    """Возвращает все события календаря в формате json"""
    events_json = []
    try:
        for event in all_events:
            raw_data = event.data
            calendar = Calendar.from_ical(raw_data)
            for component in calendar.walk('VEVENT'):
                item = {
                    "summary": get_summary(component) or "",
                    "location": get_location(component) or "",
                    "start": get_text_format_datetime(get_start_time(component)) if get_start_time(
                        component) else "",
                    "end": get_text_format_datetime(get_end_time(component)) if get_end_time(
                        component) else "",
                    "category": get_category(component) or "",
                    "description": get_description(component) or "",  #
                    "members": get_attendees_full_names(component) or "",  # Участники
                    "organizer": get_organizer_sent_by(component) or ""  # Организатор
                }

                events_json.append(item)
        return json.dumps(events_json)

    except Exception as e:
        print(f"Ошибка разбора icalendar: {e}")
