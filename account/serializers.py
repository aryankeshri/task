from rest_framework import serializers

from account.models import TaskUser


class UserResponseSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField('_get_user_role')

    def _get_user_role(self, instance):
        if instance.role == 1:
            return 'Admin'
        elif instance.role == 2:
            return 'Teacher'
        else:
            return 'Student'

    class Meta:
        model = TaskUser
        fields = ('id', 'email', 'name', 'short_name', 'last_name',
                  'role', 'email_verifed')
