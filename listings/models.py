from django.db import models


class Listing(models.Model):
    owner_name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "listing"


class Room(models.Model):
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="listings"
    )
    number = models.PositiveIntegerField(help_text="room number")
    price = models.IntegerField(help_text="price of room for one day")

    class Meta:
        ordering = ["-id"]
        db_table = "room"
        unique_together = ["listing", "number"]


class Reservation(models.Model):
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name="reservations"
    )
    name = models.CharField(max_length=100, help_text="booking name")
    from_date = models.DateField(help_text="reservation start date")
    to_date = models.DateField(help_text="reservation end date")

    class Meta:
        db_table = "reservation"
