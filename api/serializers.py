from rest_framework import serializers

from rooms.models.models import FirstRoom


class GetDataFromFirstFloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirstRoom
        fields = ["hash_value", "data_json"]
