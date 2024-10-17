import os

import caldav
from caldav.elements import dav, cdav
from datetime import datetime

# Данные для подключения к серверу
url = os.getenv("CALDAV_URL")
username = os.getenv("CALDAV_USERNAME")
password = os.getenv("CALDAV_PASSWORD")
print(url, username, password)
# Подключение к серверу
client = caldav.DAVClient(url, username=username, password=password)

print(client)

# Получаем доступ к календарям
principal = client.principal()
print(principal)
calendars = principal.calendars()
print(calendars)

if calendars:
    # Для простоты будем работать с первым календарем
    calendar = calendars[-1]

    # Получаем все события
    events = calendar.events()
    print(events)

    # Отображаем данные о встречах в консоли
    for event in events:
        # Получаем данные о событии
        event_data = event.data
        event_details = event.instance

        print(f"event_data: {event_data}")
        print(f"event_details: {event_details}")
    #
    #     # Отображаем информацию о встрече
    #     print(f"Название: {event_details.vobject_instance.vevent.summary.value}")
    #     print(f"Начало: {event_details.vobject_instance.vevent.dtstart.value}")
    #     print(f"Конец: {event_details.vobject_instance.vevent.dtend.value}")
    #     print(f"Описание: {event_details.vobject_instance.vevent.description.value}")
    #     print('-' * 50)
else:
    print("Календари не найдены")
