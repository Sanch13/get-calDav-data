import locale
import os
from dotenv import load_dotenv

import caldav

from icalendar import Calendar
from caldav.elements import dav, cdav
from datetime import datetime, timedelta

# Установка русской локали
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
# Загрузка переменных из .env
load_dotenv()

# Данные для подключения к серверу
url = os.getenv("CALDAV_URL")
username = os.getenv("CALDAV_USERNAME")
password = os.getenv("CALDAV_PASSWORD")

# date_to_search = datetime(2024, 10, 18)  # Задайте нужную дату
date_to_search = datetime.now()  # Задайте нужную дату

start_date = date_to_search - timedelta(days=1)
end_date = date_to_search + timedelta(days=1)

with caldav.DAVClient(url=url, username=username, password=password) as client:
    my_calendar = client.calendar(url=url)
    print(f"my_calendar {my_calendar}")
    # all_events = my_calendar.events()

    # Поиск событий за заданную дату
    all_events = my_calendar.date_search(start=date_to_search, end=None)

print(f"all_events {all_events}")
for event in all_events:
    raw_data = event.data
    # print(raw_data)
    try:
        calendar = Calendar.from_ical(raw_data)
        for component in calendar.walk('VEVENT'):
            summary = component.get('SUMMARY')
            location = component.get("LOCATION")
            dtstart = component.get('DTSTART').dt
            dtend = component.get("DTEND").dt
            category = component.get("CATEGORY")
            description = component.get("DESCRIPTION")
            attendee = component.get("ATTENDEE")
            print(f"\nСобытие: {summary} \n"
                  f"Место проведения: {location} \n"
                  f"Категория события: {category} \n"
                  f"Начало: {dtstart.strftime('%d %B %Y, %H:%M')} \n"
                  f"Конец: {dtend.strftime('%d %B %Y, %H:%M')} \n"
                  f"Описание: {description} \n"
                  f"Приглашенные: {attendee} \n"
                  )

            # print(f"Событие: {summary}, Начало: {dtstart}")
    except Exception as e:
        print(f"Ошибка разбора icalendar: {e}")

        # event_details = event.vobject_instance
        # contents = event_details.vevent.__dict__["contents"]
        # print()
        # for k, v in contents.items():
        #     print(f"{k}: {v}")

        # Вывод информации
        # summary = event_details.vevent.summary.value if hasattr(event_details.vevent,
        #                                                         'summary') else 'Нет темы'
        # start = event_details.vevent.dtstart.value
        # end = event_details.vevent.dtend.value if hasattr(event_details.vevent,
        #                                                   'dtend') else 'Нет времени окончания'
        # description = event_details.vevent.description.value if hasattr(event_details.vevent,
        #                                                                 'description') else 'Нет описания'
        # location = event_details.vevent.location.value if hasattr(event_details.vevent,
        #                                                           'location') else 'Нет местоположения'
        # organizer = event_details.vevent.organizer if hasattr(event_details.vevent,
        #                                                           'organizer') else 'Нет организатора'

        # Выводим данные
        # print(f"Событие: {summary}")
        # print(f"Начало: {start}")
        # print(f"Конец: {end}")
        # print(f"Описание: {description}")
        # print(f"Местоположение: {location}")
        # print(f"Организатор: {organizer}")

        # Обработка приглашенных
        # if hasattr(event_details.vevent, 'attendee'):
        #     attendees = event_details.vevent.attendee
        #     print(attendees)
        #     if isinstance(attendees, list):
        #         for attendee in attendees:
        #             print(f"Приглашенный: {attendee.value}")
        #     else:
        #         print(f"Приглашенный: {attendees.value}")
        #
        # print()
        # print()
# # Подключение к серверу
# client = caldav.DAVClient(url, username=username, password=password)
#
# print(client)  # <caldav.davclient.DAVClient object at 0x7f076c838810>
#
# # Получаем доступ к календарям
# principal = client.principal()
# print(f"principal {principal}")
# calendars = principal.calendars()
# print(f"calendars[-1] {calendars[-1]}")





# if calendars:
#     # Для простоты будем работать с первым календарем
#     calendar = calendars[-1]
#
#     # Получаем все события
#     events = calendar.events()
#     print(events)
#
#     # Отображаем данные о встречах в консоли
#     for event in events:
#         # Получаем данные о событии
#         event_data = event.data
#         event_details = event.instance
#
#         print(f"event_data: {event_data}")
#         print(f"event_data__dict__: {dir(event_data)}")
#         # print(f"event_details: {event_details}")
#     #
#     #     # Отображаем информацию о встрече
#     #     print(f"Название: {event_details.vobject_instance.vevent.summary.value}")
#     #     print(f"Начало: {event_details.vobject_instance.vevent.dtstart.value}")
#     #     print(f"Конец: {event_details.vobject_instance.vevent.dtend.value}")
#     #     print(f"Описание: {event_details.vobject_instance.vevent.description.value}")
#     #     print('-' * 50)
# else:
#     print("Календари не найдены")
