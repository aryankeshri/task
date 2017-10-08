from rest_framework import serializers

from account.models import TaskUser
from .models import Task, TaskAssignUser


class TaskUserSerializer(serializers.ModelSerializer):
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
        fields = ('id', 'email', 'role')


class TaskSerializer(serializers.ModelSerializer):
    created_by = TaskUserSerializer()

    class Meta:
        model = Task
        fields = '__all__'


class TaskAssignUserSerializer(serializers.ModelSerializer):
    user = TaskUserSerializer()

    class Meta:
        model = TaskAssignUser
        fields = '__all__'
