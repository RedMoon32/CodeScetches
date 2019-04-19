from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
        This is temporarily csrf excluding middleware, before the moment i explain Abdelrahman that some one can steal
        our cookies stored in http only.
    """
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening
