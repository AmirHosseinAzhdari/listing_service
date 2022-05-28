from django.urls import path
from rest_framework import routers
from . import views

app_name = "listings"

urlpatterns = [
    path(
        "room/available/", views.AvailableRoomsListView.as_view(), name="room-available"
    ),
    path("room/reserve/", views.ReservationView.as_view(), name="room-reserve"),
    path("room/report/", views.ReservationRoomListView.as_view(), name="room-report"),
]

router = routers.SimpleRouter()
router.register("", views.ListingViewSet)
router.register("room", views.RoomViewSet)
urlpatterns += router.urls
