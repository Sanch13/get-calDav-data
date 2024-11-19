from rest_framework import serializers

from rooms.models.models import FirstRoom, ThirdRoom


class GetDataFromFirstFloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirstRoom
        fields = ["hash_value", "data_json"]


class GetDataFromThirdFloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThirdRoom
        fields = ["hash_value", "data_json"]