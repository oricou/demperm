from dataclasses import dataclass

from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions


@dataclass
class SimpleUser:
    id: str

    @property
    def is_authenticated(self) -> bool:
        # TODO: Obligatoire. A changer plus tard avec vrai authent
        return True


class SimpleBearerAuthentication(BaseAuthentication):
    """
    Auth simplifiée :
    - Attend un header: Authorization: Bearer <user-id>
    - Ne vérifie pas de JWT, juste la présence du token
    """

    keyword = "Bearer"

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        parts = auth_header.split()

        if len(parts) != 2 or parts[0] != self.keyword:
            raise exceptions.AuthenticationFailed("Invalid Authorization header")

        token = parts[1].strip()

        if not token:
            raise exceptions.AuthenticationFailed("Empty bearer token")

        user = SimpleUser(id=token)
        return user, None
