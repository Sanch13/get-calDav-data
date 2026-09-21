import datetime

import requests

from b24pysdk.errors import BitrixAPIError, BitrixSDKException
from b24pysdk import Client, BitrixWebhook
from b24pysdk import Config
from b24pysdk.log import StreamLogger

from rooms.utils import get_sorted_all_events_from_bitrix, get_all_events_today_in_json

Config().configure(logger=StreamLogger())

BITRIX_DOMAIN = "bitrix.miran-bel.com"
BITRIX_WEBHOOK_USER_ID = 226
BITRIX_WEBHOOK_KEY = "yyejq8bt6p3hn4aq"
BITRIX_WEBHOOK_TOKEN = f"{BITRIX_WEBHOOK_USER_ID}/{BITRIX_WEBHOOK_KEY}"
BITRIX_FIRST_SECTION_ID = 54
BITRIX_CUP_SECTION_ID = 56
BITRIX_THIRD_SECTION_ID = 55
BITRIX_CLASSROOM_SECTION_ID = 97


def get_bitrix_client() -> Client:
    token = BitrixWebhook(
        domain=BITRIX_DOMAIN,
        webhook_token=BITRIX_WEBHOOK_TOKEN,
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
        result.append({
            "organizer": ev.get("NAME", ""),
            "summary": parent.get("NAME") or ev.get("NAME", ""),
            "start": ev.get("DATE_FROM", ""),
            "end": ev.get("DATE_TO", ""),
        })
    return result


def main(client, payload):
    try:
        request = client.calendar.event.get(**payload)
        result = request.result
        print(result)
    except BitrixAPIError as error:
        print(
            "Ошибка Bitrix API",
            f"error: {error.error}",
            f"error_description: {error.error_description}",
            sep="\n",
        )
    except BitrixSDKException as error:
        print(f"Ошибка Bitrix SDK: {error.message}")
    except Exception as error:
        print(f"Непредвиденная ошибка: {error}")


if __name__ == '__main__':
    now = datetime.datetime.now().strftime("%Y-%m-%d")
    section_id = BITRIX_FIRST_SECTION_ID

    client = get_bitrix_client()
    raw_events = get_raw_events(client, section_id, now, now)
    events_room = get_room_events_json(raw_events)
    sorted_all_events_today = get_sorted_all_events_from_bitrix(events_room)
    data = get_all_events_today_in_json(sorted_all_events_today)
