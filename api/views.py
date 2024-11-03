from datetime import datetime

from rest_framework import views
from rest_framework.views import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from api.serializers import GetDataFromFirstFloorSerializer

from rooms.models.models import FirstRoom

from rooms.utils import (
    get_caldav_config,
    connect_to_calendar,
    get_sorted_events,
    get_sorted_all_events,
    generate_hash,
    get_all_events_today_in_json
)


class GetCurrentEventsAPIView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        print("API")
        events_today = connect_to_calendar(**get_caldav_config()).date_search(start=datetime.now())
        sorted_events_today = get_sorted_events(events_today)
        sorted_all_events_today = get_sorted_all_events(sorted_events_today)
        hash_value = generate_hash(sorted_all_events_today)

        try:
            if not FirstRoom.objects.filter(hash_value=hash_value).exists():
                print("API - СОЗДАЮ НОВУЮ ЗАПИСЬ в БД")
                all_events_today_json = get_all_events_today_in_json(sorted_all_events_today)
                serializer = GetDataFromFirstFloorSerializer(data={
                    "hash_value": hash_value,
                    "data_json": all_events_today_json,
                })
                if serializer.is_valid(raise_exception=True):
                    serializer.save()

            instance = FirstRoom.objects.get(hash_value=hash_value)
        except FirstRoom.DoesNotExist:
            return Response(data={"error": "Object not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = GetDataFromFirstFloorSerializer(instance)
        return Response(data=serializer.data,
                        status=status.HTTP_200_OK)
