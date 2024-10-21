import locale

import caldav

from icalendar import Calendar
from datetime import datetime, timedelta

from utils import (
    get_text_format_datetime,
    get_organizer_sent_by,
    get_attendees_full_names,
    get_caldav_config,
    connect_to_calendar,
    get_summary,
    get_location,
    get_start_time,
    get_end_time,
    get_category,
    get_description, get_carddav_contacts
)

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')  # Установка русской локали

credentials = get_caldav_config()

# date_to_search = datetime(2024, 10, 18)  # Задайте нужную дату
date_to_search = datetime.now()  # Задайте нужную дату

start_date = date_to_search - timedelta(days=1)
end_date = date_to_search + timedelta(days=1)

my_calendar = connect_to_calendar(**credentials)  # <class 'caldav.objects.Calendar'>

all_events = my_calendar.date_search(start=date_to_search, end=None)

for event in all_events:
    raw_data = event.data
    try:
        calendar = Calendar.from_ical(raw_data)
        for component in calendar.walk('VEVENT'):
            summary = get_summary(component)
            location = get_location(component)
            start = get_text_format_datetime(get_start_time(component)) if get_start_time(component) else ""
            end = get_text_format_datetime(get_end_time(component)) if get_end_time(component) else ""
            category = get_category(component)
            description = get_description(component)  #
            members = get_attendees_full_names(component)  # Участники
            organizer = get_organizer_sent_by(component)  # Организатор

            print(f"\nСобытие: {summary} \n"
                  f"Место проведения: {location} \n"
                  f"Категория события: {category} \n"
                  f"Начало: {start} "
                  f"Конец: {end} \n"
                  f"Описание: {description} \n"
                  f"Организатор: {organizer} \n"
                  f"Приглашенные: {members} \n"
                  )

            # print(f"Событие: {summary}, Начало: {dtstart}")
    except Exception as e:
        print(f"Ошибка разбора icalendar: {e}")


contacts = get_carddav_contacts(**get_caldav_config())
for contact in contacts:
    print(f"Имя: {contact['name']}, Email: {contact['email']}")
