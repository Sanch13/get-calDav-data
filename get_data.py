import locale

from datetime import datetime
from utils import (
    get_caldav_config,
    connect_to_calendar,
    get_all_events_json,
)

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')  # Установка русской локали

credentials = get_caldav_config()

date_to_search = datetime.now()  # Задайте нужную дату

all_events = connect_to_calendar(**credentials).date_search(start=date_to_search,
                                                            end=None)  # <class 'caldav.objects.Calendar'>

events_json = get_all_events_json(all_events)

if __name__ == '__main__':
    print(events_json)

