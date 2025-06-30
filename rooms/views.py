import datetime

from django.shortcuts import render

from logs.logging_config import logger


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
