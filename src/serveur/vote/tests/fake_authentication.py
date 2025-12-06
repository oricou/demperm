from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

class FakeAuthentication(BaseAuthentication):
    """
    Utilisée uniquement en tests.
    Simule Firebase : Authorization: Bearer <uid> → user.id = <uid>
    """

    class FakeUser:
        def __init__(self, uid):
            self.id = uid
            self.is_authenticated = True

    def authenticate(self, request):
        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Bearer "):
            raise AuthenticationFailed("No credentials")

        uid = auth.removeprefix("Bearer ").strip()

        user = self.FakeUser(uid)
        return (user, None)
