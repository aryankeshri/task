import base64
import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework import status
from rest_framework import views
from rest_framework import viewsets
from rest_framework.response import Response
from django.utils.translation import ugettext as _

from account.models import TaskUser, Token
from account.serializers import UserResponseSerializer
from core.api_permissions import has_permission
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


class ChangePasswordView(viewsets.ModelViewSet):

    def check_old_password(self, user, value):
        if user.check_password(value):
            return True
        else:
            return False

    def post(self, request):
        """
        In header token
        :param request: old_password, new_password
        :return: new_token = token, message
        """
        user = has_permission(request)
        old_password = request.data['old_password']
        new_password = request.data['new_password']
        if old_password and new_password is not None:
            validate = self.check_old_password(user, old_password)
            if validate:
                user.set_password(new_password)
                user.save()
                content = {
                    'token': jwt_encode_handler(jwt_payload_handler(user)),
                    'message': _("New password has been saved.")
                }
                return Response(content, status=status.HTTP_200_OK)
            else:
                return Response({"message": _("Old password is not correct!"), },
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": _("fields are required!!"), },
                            status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(viewsets.ModelViewSet):

    def reset(self, request):
        """
        First step of forget password.
        In mail it sends user short name, token, uid(formatted), domain(site domain)
        :param request: email
        :return: message
        """
        email = request.data['email']
        try:
            user = TaskUser.objects.get(email__iexact=email)
            uid = base64.urlsafe_b64encode(force_bytes(user.id)).rstrip(b'\n=')
            token = uuid.uuid4().hex
            get, created = Token.objects.get_or_create(uid=user.id)
            get.token = token
            get.status = False
            get.save()
            # subject = 'Task password reset request'
            # template = 'reset_password.html'
            # recipients = [user.email]
            # context = {
            #     'username': user.username,
            #     'token': token,
            #     'uid': uid,
            #     'domain': str(get_site(self.request))
            # }
            # email_send(subject, template, recipients, context)
            # return Response({'message': _("Password reset e-mail has been sent."), },
            #                 status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': _("user doesn't exist!!")},
                            status=status.HTTP_200_OK)

    def reset_done(self, request):
        """
        Second step of reset password after clicking link which sent by server .
        :param request: uid, token, new_password
        :return: message
        """
        uid = request.data['uid']
        token = request.data['token']
        password = request.data['new_password']
        user_id = force_text(urlsafe_base64_decode(uid))
        try:
            token_obj = Token.objects.get(uid=user_id, token=token)
            if token_obj.status is not True:
                user = TaskUser.objects.get(id=user_id)
                user.set_password(password)
                user.save()
                token_obj.status = True
                token_obj.save()
                # subject = 'Task password reset request done'
                # template = 'reset_password_done.html'
                # recipients = [user.email]
                # context = {
                #     'username': user.short_name(),
                # }
                # email_send(subject, template, recipients, context)
                return Response({"message": _("Password reset with the new password.")},
                                status=status.HTTP_200_OK)
            else:
                return Response({"message": _("This link used.")},
                                status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'message': _('Token not exist'), },
                            status=status.HTTP_404_NOT_FOUND)


class Logout(views.APIView):

    def get(self, request):
        """
        Its store logout time of user
        :param request: header(token)
        :return: message
        """
        user = has_permission(request)
        user.last_login = timezone.now()
        user.save()
        context = {
         'message': 'successfully logout!!'
        }
        return Response(context, status=status.HTTP_200_OK)
