from django.core.exceptions import ObjectDoesNotExist

from account.models import TaskUser
from core.encryption import crypto_encode


def is_authenticate(username, password):
    """
    Authenticate the user
    1. on the basis of email + password
    2. on the basis of username + password + company link
    :param username: required(email/username)
    :param password: required
    :return: if success user object, otherwise pass
    """
    try:
        user = TaskUser.objects.get(email__iexact=username)
        if user.check_password(password):
            user.token = crypto_encode(user.id)
            user.save()
            return user
    except ObjectDoesNotExist:
        pass
