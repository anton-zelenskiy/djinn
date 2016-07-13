from django.contrib.auth import get_user_model


class EmailAuthBackend(object):
    """
    A custom authentication backend. Allows users to log in using their email address.
    """

    def authenticate(self, email=None, password=None):
        """
        Authentication method
        :param password:
        :param email:
        """
        try:
            user = get_user_model().objects.get(email=email)
            if user.check_password(password):
                return user
        except get_user_model().DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = get_user_model().objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except get_user_model().DoesNotExist:
            return None
