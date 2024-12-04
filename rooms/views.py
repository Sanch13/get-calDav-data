import datetime

from django.shortcuts import render

from logs.logging_config import logger


def first_room(request):
    logger.info(f"Перезагрука первой комнаты {datetime.datetime.now().strftime('%d %B %Y %H:%M:%S')}")
    return render(request=request,
                  template_name="rooms/first.html")


def third_room(request):
    logger.info(f"Перезагрука третьей комнаты {datetime.datetime.now().strftime('%d %B %Y %H:%M:%S')}")
    return render(request=request,
                  template_name="rooms/third.html")
