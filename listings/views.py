from rest_framework import status, viewsets, generics, views
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .authentication import ListingValidateAuthentication
from .helper import validate_date_format, validate_room_in_listing
from .models import Room, Reservation, Listing
from .serializer import (
    RoomSerializer,
    ReservationSerializer,
    ReportRoomSerializer,
    ListingSerializer,
)


class ListingViewSet(viewsets.ViewSet):
    model_name = Listing
    queryset = model_name.objects.all()
    serializer_class = ListingSerializer

    def list(self, request):
        serializer = self.serializer_class(self.model_name.objects.all(), many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="listing",
            type=int,
            location=OpenApiParameter.HEADER,
            description="listing id",
        ),
    ]
)
class RoomViewSet(viewsets.ViewSet):
    model_name = Room
    queryset = model_name.objects.all()
    serializer_class = RoomSerializer
    authentication_classes = [ListingValidateAuthentication]

    def list(self, request):
        queryset = self.model_name.objects.filter(
            listing=int(self.request.headers["listing"])
        )
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        data = request.data
        data["listing"] = int(self.request.headers["listing"])
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        self.model_name.objects.filter(pk=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="listing",
            type=int,
            location=OpenApiParameter.HEADER,
            description="listing id",
        ),
    ]
)
class AvailableRoomsListView(generics.ListAPIView):
    serializer_class = RoomSerializer
    authentication_classes = [ListingValidateAuthentication]

    def get_queryset(self):
        date = self.request.query_params.get("date")
        if date not in ["", None] and validate_date_format(date):
            rooms = Room.objects.filter(listing=int(self.request.headers["listing"]))
            reservations_on_date = Reservation.objects.filter(
                room__listing=int(self.request.headers["listing"]),
                from_date__lte=date,
                to_date__gte=date,
            ).values("room")
            reserved_ids = [i["room"] for i in reservations_on_date]
            return [r for r in rooms if r.id not in reserved_ids]
        return []


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="listing",
            type=int,
            location=OpenApiParameter.HEADER,
            description="listing id",
        ),
    ]
)
class ReservationView(views.APIView):
    authentication_classes = [ListingValidateAuthentication]

    @extend_schema(
        request=ReservationSerializer,
        responses={201: ReservationSerializer},
    )
    def post(self, request):
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            if not validate_room_in_listing(
                int(request.headers["listing"]), serializer.validated_data["room"].id
            ):
                return Response(
                    {"room": "room does not exist in current listing"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="listing",
            type=int,
            location=OpenApiParameter.HEADER,
            description="listing id",
        ),
    ]
)
class ReservationRoomListView(generics.ListAPIView):
    serializer_class = ReportRoomSerializer
    authentication_classes = [ListingValidateAuthentication]

    def get_queryset(self):
        return Room.objects.filter(listing=int(self.request.headers["listing"]))
