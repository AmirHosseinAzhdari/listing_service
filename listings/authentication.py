from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from listings.helper import validate_listing


class ListingValidateAuthentication(BaseAuthentication):
    def authenticate(self, request):
        if not validate_listing(request.headers.get("listing")):
            raise AuthenticationFailed("Invalid request")
