from datetime import datetime

from .models import Reservation, Listing, Room


def check_room_reserved(room_id: int, from_date: str, to_date: str) -> bool:
    """Check if a room reservation exists in database in defined date range

    Args:
        room_id (int): id of room
        from_date (str): start date
        to_date (str): end date

    Returns:
        bool: if exists returns True else False
    """
    if Reservation.objects.filter(room__id=room_id, from_date__lte=to_date, to_date__gte=from_date).exists():
        return True
    return False


def validate_date_format(date: str) -> bool:
    """Validate a date format must be 'YYYY-MM-DD'

    Args:
        date (str): date for validating

    Returns:
        bool: True for valid date and False for invalid date
    """
    try:
        datetime.strptime(str(date), "%Y-%m-%d")
    except ValueError:
        return False
    return True


def validate_date_range(start_date: str, end_date: str) -> bool:
    """Validate order of date 

    Args:
        start_date (str): smaller date
        end_date (str): bigger date

    Returns:
        bool: False if start date is biggest and True if end date is biggest
    """
    if datetime.strptime(str(start_date), '%Y-%m-%d') > datetime.strptime(str(end_date), '%Y-%m-%d'):
        return False
    return True


def validate_listing(listing_id: str) -> bool:
    if listing_id and listing_id.isnumeric() and Listing.objects.filter(id=int(listing_id)).exists():
        return True
    return False


def validate_room_in_listing(listing_id: int, room_id: int) -> bool:
    if Room.objects.filter(listing=listing_id, id=room_id).exists():
        return True
    return False
