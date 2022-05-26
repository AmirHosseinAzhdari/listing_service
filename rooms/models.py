from django.db import models


class Room(models.Model):
    number = models.PositiveIntegerField(help_text="room number", unique=True)
    price = models.IntegerField(help_text="price of room for one day")

    class Meta:
        db_table = "room"


class Reservation(models.Model):
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name="income_factors"
    )
    name = models.CharField(max_length=100, help_text="booking name")
    from_date = models.DateField(help_text="reservation start date")
    to_date = models.DateField(help_text="reservation end date")

    class Meta:
        db_table = "reservation"
