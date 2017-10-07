from rest_framework import serializers
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from django.utils.translation import ugettext as _

from account.models import TaskUser
from account.serializers import UserResponseSerializer
from core.authentication import is_authenticate
from core.encryption import jwt_payload_handler, jwt_encode_handler


class SignUpView(viewsets.ModelViewSet):

    def register(self, request):
        email = request.data['email'].lower()
        check = TaskUser.objects.filter(email__iexact=email).exists()
        if check:
            content = {
                'message': 'Already Exist'
            }
            return Response(content, status=status.HTTP_409_CONFLICT)

        password = request.data['password']
        full_name = str.title(request.data['full_name'])
        role = request.data['role']
        if role == 1:
            role = 1
        elif role == 2:
            role = 2
        else:
            role = 3

        extra_fields = {
            'full_name': full_name,
            'role': role
        }
        user = TaskUser.objects.create_user(email=email,
                                            password=password,
                                            **extra_fields)
        payload = jwt_payload_handler(user)
        content = {
            'token': jwt_encode_handler(payload),
            'user': UserResponseSerializer(user, context={'request': request}).data
        }
        return Response(content, status=status.HTTP_200_OK)


class Login(viewsets.ModelViewSet):

    def post(self, request):
        """
        Login the user user with username(email/username), password
        :param request: email, password
        :return: token, user
        """
        username = request.data['email']
        password = request.data['password']
        user = is_authenticate(username, password)
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise serializers.ValidationError(msg)
            payload = jwt_payload_handler(user)
            content = {
                'token': jwt_encode_handler(payload),
                'user': UserResponseSerializer(user, context={'request': request}).data
            }
            return Response(content, status=status.HTTP_200_OK)
        else:
            msg = _('Unable to login with provided credentials.')
            raise serializers.ValidationError(msg)