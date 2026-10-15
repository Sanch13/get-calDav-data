import datetime
import logging
from functools import lru_cache

from b24pysdk import Client, BitrixWebhook

from django.conf import settings

from rooms.utils import parse_bitrix_datetime, BITRIX_DATE_FORMAT
from rooms.services.telegram import send_telegram_message  # noqa: F401  (реэкспорт)

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_bitrix_client() -> Client:
    token = BitrixWebhook(
        domain=settings.BITRIX_DOMAIN,
        webhook_token=settings.BITRIX_WEBHOOK_TOKEN,
    )
    return Client(token)


def get_raw_events(client, section_id: int, from_day: str, to_day: str) -> list:
    request = client.calendar.event.get(
        type="location",
        owner_id=0,
        from_date=from_day,
        to=to_day,
        section=[section_id],
    )
    return request.result


def get_room_events_json(client, raw_events) -> list[dict]:
    parent_ids = {ev["PARENT_ID"] for ev in raw_events if ev.get("PARENT_ID")}

    parents_by_id = {}
    if parent_ids:
        requests_data = {
            f"ev_{pid}": client.calendar.event.get_by_id(bitrix_id=int(pid))
            for pid in parent_ids
        }
        batch_request = client.call_batch(requests_data)
        for _, parent_event in batch_request.result.result.items():
            parents_by_id[parent_event["ID"]] = parent_event

    result = []
    for ev in raw_events:
        parent = parents_by_id.get(ev.get("PARENT_ID"), {})

        start_raw = ev.get("DATE_FROM", "")
        end_raw = ev.get("DATE_TO", "")

        # Событие "весь день": Bitrix отдаёт DATE_FROM == DATE_TO,
        # реальная длительность — в DT_LENGTH (секунды).
        if ev.get("DT_SKIP_TIME") == "Y" and start_raw:
            start_dt = parse_bitrix_datetime(start_raw)
            length = ev.get("DT_LENGTH") or 86400
            end_dt = start_dt + datetime.timedelta(seconds=length)
            end_raw = end_dt.strftime(BITRIX_DATE_FORMAT)

        result.append({
            "organizer": ev.get("NAME", ""),
            "summary": parent.get("NAME") or ev.get("NAME", ""),
            "start": start_raw,
            "end": end_raw,
        })
    return result

# if __name__ == '__main__':
#     import os
#     import django
#
#     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
#     django.setup()
#     send_telegram_message("TEST-2")


# now = datetime.datetime.now().strftime("%Y-%m-%d")
# section_id = settings.MEETING_ROOMS["first"]["bitrix_resource_id"]
# print(section_id)
# client = get_bitrix_client()
# raw_events = get_raw_events(client, section_id, now, now)
# events_room = get_room_events_json(client, raw_events)
# sorted_all_events_today = get_sorted_all_events_from_bitrix(events_room)
# print(sorted_all_events_today)
# data = get_all_events_today_in_json(sorted_all_events_today)
