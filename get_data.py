import json
import locale

from datetime import datetime
from utils import (
    get_caldav_config,
    connect_to_calendar,
    get_sorted_all_events,
    get_all_events_in_json
)

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')  # Установка русской локали

credentials = get_caldav_config()

date_now = datetime.now()

all_events_now = connect_to_calendar(**credentials).date_search(start=date_now,
                                                                end=None)  # <class 'caldav.objects.Calendar'>

if __name__ == '__main__':

    sorted_events = get_sorted_all_events(all_events_now)
    all_events_cur_day = get_all_events_in_json(sorted_events)

    with open("example.json", "w", encoding="utf-8") as file:
        file.write(all_events_cur_day)

    with open("example.json", "r", encoding="utf-8") as file:
        all_data = json.loads(file.read())

    for event in all_data:
        print(datetime.fromisoformat(event["start"]).strftime("%H:%M"),
              datetime.fromisoformat(event["end"]).strftime("%H:%M"),
              event["status"],
              event["summary"])
