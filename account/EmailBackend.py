from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackendCustom(ModelBackend):
    """
    Вход по электронной почте

    """
    def __init__(self):
        self.UserModel = get_user_model()

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = self.UserModel.objects.get(email=username)
        except self.UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None

