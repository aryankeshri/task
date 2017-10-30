from django.shortcuts import get_object_or_404
from rest_framework import exceptions

from account.models import TaskUser
from .encryption import (jwt_decode_handler, crypto_decode)


# def has_permission(request):
#     if 'HTTP_AUTHORIZATION' in request.META:
#         user_id = crypto_decode(
#                 jwt_decode_handler(
#                     request.META['HTTP_AUTHORIZATION']
#                 )['id']
#         )
#         user = TaskUser.objects.get(id=int(user_id))
#         return user
#     else:
#         raise exceptions.NotAcceptable('Not allowed!!')


def has_permission(request):
    if 'HTTP_AUTHORIZATION' in request.META:
        user = get_object_or_404(TaskUser, token=request.META['HTTP_AUTHORIZATION'])
        return user
    else:
        raise exceptions.NotAcceptable('Not allowed!!')