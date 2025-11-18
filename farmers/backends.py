# farmers/backends.py
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import FarmerAccount

class FarmerBackend(BaseBackend):
    """
    Authenticate FarmerAccount using email (case-insensitive).
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        # allow passing email kwarg or username param
        email = kwargs.get('email') or username
        if not email or not password:
            return None
        try:
            # case-insensitive lookup
            user = FarmerAccount.objects.get(email__iexact=email)
        except FarmerAccount.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def get_user(self, user_id):
        try:
            return FarmerAccount.objects.get(pk=user_id)
        except FarmerAccount.DoesNotExist:
            return None

    def user_can_authenticate(self, user):
        """
        Mirrors Django's ModelBackend.user_can_authenticate: ensure is_active
        """
        is_active = getattr(user, "is_active", None)
        return is_active or is_active is None
