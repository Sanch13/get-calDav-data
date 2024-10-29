import hashlib
import json
from datetime import datetime, timedelta

from django.shortcuts import render, get_object_or_404

from rest_framework import views
from rest_framework.permissions import AllowAny

from rooms.utils import (
    get_caldav_config,
    generate_hash,
    connect_to_calendar,
    get_sorted_all_events,
    get_all_events_in_json
)
from rooms.models.models import FirstRoom


class TheFirstConferenceView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        credentials = get_caldav_config()
        date_today = datetime.now()  # 2024-10-29
        all_events_today = connect_to_calendar(**credentials).date_search(start=date_today,
                                                                          end=None)
        sorted_events_today = get_sorted_all_events(all_events_today)
        all_events_today_json = get_all_events_in_json(sorted_events_today)
        print(all_events_today_json)
        hash_value = generate_hash(all_events_today_json)

        if not FirstRoom.objects.filter(hash_value=hash_value).exists():
            print("Created object to DB")
            FirstRoom.objects.create(hash_value=hash_value,
                                     data_json=all_events_today_json)

        context = {
            "data": get_object_or_404(FirstRoom, hash_value=hash_value).data_json
        }

        return render(request=request,
                      template_name="rooms/index_old.html",
                      context=context)
