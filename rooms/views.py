import datetime

from django.shortcuts import render
from django.http import Http404
from django.urls import reverse
from django.conf import settings

from logs.logging_config import logger


def room_view(request, room_slug: str):
    room = settings.MEETING_ROOMS.get(room_slug)
    if room is None:
        raise Http404("Комната не найдена")

    logger.info(f"Загрузка страницы комнаты {room_slug} — {datetime.datetime.now():%d %B %Y %H:%M:%S}")

    return render(request, "rooms/room.html", {
        "room": room,
        "api_events_url": reverse("api:api-room-events", kwargs={"room_slug": room_slug}),
    })


def first_room(request):
    logger.info(f"Перезагрука первой комнаты {datetime.datetime.now().strftime('%d %B %Y %H:%M:%S')}")
    return render(request=request,
                  template_name="rooms/first.html")


def second_room(request):
    logger.info(f"Перезагрука второй комнаты {datetime.datetime.now().strftime('%d %B %Y %H:%M:%S')}")
    return render(request=request,
                  template_name="rooms/second.html")


def third_room(request):
    logger.info(f"Перезагрука третьей комнаты {datetime.datetime.now().strftime('%d %B %Y %H:%M:%S')}")
    return render(request=request,
                  template_name="rooms/third.html")


def class_room(request):
    logger.info(f"Перезагрука Учебной комнаты {datetime.datetime.now().strftime('%d %B %Y %H:%M:%S')}")
    return render(request=request,
                  template_name="rooms/class_room.html")
