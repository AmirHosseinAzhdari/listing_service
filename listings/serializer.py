from rest_framework import serializers

from .helper import validate_date_range, check_room_reserved
from .models import Room, Reservation, Listing


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = "__all__"


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"

    def validate(self, attrs):
        if not validate_date_range(attrs["from_date"], attrs["to_date"]):
            raise serializers.ValidationError({"from_date": "from date must smaller than equal from to date"})
        if check_room_reserved(attrs["room"].id, attrs["from_date"], attrs["to_date"]):
            raise serializers.ValidationError({"room": "reservation for this room in defined time already exist"})
        return attrs


class ReportRoomSerializer(serializers.ModelSerializer):
    reservations = ReservationSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ["number", "price", "reservations"]
