from django.urls import path
from . import views
from rest_framework import routers

app_name = "rooms"

urlpatterns = [
    # path("", views.IncomeFactorView.as_view(), name="income_factor"),
]

router = routers.SimpleRouter()
router.register("", views.RoomViewSet)
urlpatterns += router.urls
