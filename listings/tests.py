from django.test import TestCase

from listings.helper import (
    check_room_reserved,
    validate_date_format,
    validate_date_range,
    validate_listing,
    validate_room_in_listing,
)
from listings.models import Reservation, Room, Listing


class CheckRoomReservedTest(TestCase):
    def setUp(self):
        listing = Listing.objects.create(owner_name="test name")
        room = Room.objects.create(listing=listing, number=1, price=200)
        Reservation.objects.create(
            room=room,
            name="test room name",
            from_date="2022-05-24",
            to_date="2022-05-26",
        )

    def test_with_reserved_date(self):
        """If reservation exist for defined date function must return True"""
        room = Room.objects.get(number=1)
        date_in_reserved = [
            ("2022-05-24", "2022-05-26"),
            ("2022-05-23", "2022-05-25"),
            ("2022-05-25", "2022-05-27"),
            ("2022-05-23", "2022-05-27"),
        ]
        for date in date_in_reserved:
            res = check_room_reserved(
                room_id=room.id, from_date=date[0], to_date=date[1]
            )
            self.assertEqual(res, True)

    def test_with_doesnt_reserved_date(self):
        """If reservation not exist for defined date function must return False"""
        room = Room.objects.get(number=1)
        date_in_reserved = [("2022-05-20", "2022-05-23"), ("2022-05-27", "2022-05-28")]
        for date in date_in_reserved:
            res = check_room_reserved(
                room_id=room.id, from_date=date[0], to_date=date[1]
            )
            self.assertEqual(res, False)


class ValidateDateFormatTest(TestCase):
    def test_with_invalid_date_format(self):
        """If date is in invalid format (not YYYY-MM-DD) and invalid date function must return False"""
        invalid_dates = [
            "2022-25--24",
            "202-25-24",
            "2022/25/24",
            "2022-25-25",
            "2022-05-32",
        ]
        for date in invalid_dates:
            res = validate_date_format(date)
            self.assertEqual(res, False)

    def test_with_valid_date_format(self):
        """If date is in valid format (YYYY-MM-DD) and valid date function must return True"""
        valid_date = "2022-05-25"
        res = validate_date_format(valid_date)
        self.assertEqual(res, True)


class ValidateDateRangeTest(TestCase):
    def test_with_smaller_and_equal_start_date(self):
        """If start date is smaller than or equal end date function must return True"""
        start_dates = ["2022-05-01", "2022-05-02"]
        end_date = "2022-05-02"
        for date in start_dates:
            res = validate_date_range(start_date=date, end_date=end_date)
            self.assertEqual(res, True)

    def test_with_bigger_start_date(self):
        """If start date is bigger than end date function must return False"""
        start_date = "2022-05-03"
        end_date = "2022-05-02"
        res = validate_date_range(start_date=start_date, end_date=end_date)
        self.assertEqual(res, False)


class ValidateListingTest(TestCase):
    def setUp(self):
        Listing.objects.create(owner_name="test name")

    def test_with_invalid_listing_id(self):
        """If listing_id is null, invalid(not integer string) function must return False"""
        invalid_listing_ids = ["sa", None, "", "1s"]
        for i in invalid_listing_ids:
            res = validate_listing(listing_id=i)
            self.assertEqual(res, False)

    def test_with_listing_not_exist(self):
        """If listing not exists in database with defined listing_id function must return False"""
        listing = Listing.objects.get(owner_name="test name")
        res = validate_listing(listing_id=str(listing.id + 1))
        self.assertEqual(res, False)

    def test_with_valid_id_and_listing_is_exists(self):
        """If listing_id is valid and exists in database function must return True"""
        listing = Listing.objects.get(owner_name="test name")
        res = validate_listing(listing_id=str(listing.id))
        self.assertEqual(res, True)


class ValidateRoomInListingTest(TestCase):
    def setUp(self):
        listing = Listing.objects.create(owner_name="test name")
        Room.objects.create(listing=listing, number=1, price=200)

    def test_with_room_not_exists(self):
        """If room does not exist function must return False"""
        listing = Listing.objects.get(owner_name="test name")
        room = Room.objects.get(number=1)
        params = [
            (listing.id + 1, room.id + 1),
            (listing.id, room.id + 1),
            (listing.id + 1, room.id),
        ]
        for p in params:
            res = validate_room_in_listing(p[0], p[1])
            self.assertEqual(res, False)

    def test_with_room_exists(self):
        """If room exist, function must return True"""
        listing = Listing.objects.get(owner_name="test name")
        room = Room.objects.get(number=1)
        res = validate_room_in_listing(listing.id, room.id)
        self.assertEqual(res, True)
