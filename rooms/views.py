from datetime import datetime

from django.shortcuts import render, get_object_or_404

from rest_framework import views
from rest_framework.permissions import AllowAny

from rooms.utils import (
    get_caldav_config,
    generate_hash,
    connect_to_calendar,
    get_sorted_events,
    get_sorted_all_events,
    get_all_events_today_in_json,
)
from rooms.models.models import FirstRoom


class TheFirstConferenceView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        print("USUAL REQUEST")

        # events_today = connect_to_calendar(**get_caldav_config()).date_search(start=datetime.now())
        # sorted_events_today = get_sorted_events(events_today)
        # sorted_all_events_today = get_sorted_all_events(sorted_events_today)
        # hash_value = generate_hash(sorted_all_events_today)
        #
        # if not FirstRoom.objects.filter(hash_value=hash_value).exists():
        #     print("USUAL REQUEST СОЗДАЮ НОВУЮ ЗАПИСЬ в БД")
        #     all_events_today_json = get_all_events_today_in_json(sorted_all_events_today)
        #     FirstRoom.objects.create(hash_value=hash_value,
        #                              data_json=all_events_today_json)
        #
        # context = {
        #     "data": get_object_or_404(FirstRoom, hash_value=hash_value).data_json,
        # }
        return render(request=request,
                      template_name="rooms/first.html")


class TheThirdConferenceView(views.APIView):
    def get(self, request):
        print("USUAL REQUEST")

        return render(request=request,
                      template_name="rooms/third.html")