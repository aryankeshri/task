from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.response import Response

from account.models import TaskUser
from assignments.serializers import TaskSerializer, TaskAssignUserSerializer
from core.api_permissions import has_permission
from .models import Task, TaskAssignUser


class TaskView(viewsets.ModelViewSet):

    def create_task(self, request):
        """
        create task method
        :param request:
            header = jwt token
            data = {
                question: 'abcd ?',
                assign_user: [
                    {
                        email: yz@gmail.com
                    },
                    {
                        email: yz@gmail.com
                    },
                    {
                        email: yz@gmail.com
                    }
                ]
            }
        :return: response
        """
        user_perm = has_permission(request)
        if user_perm.role == (1 or 2):
            task_obj = Task.objects.create(question=request.data['question'],
                                           created_by=user_perm.id
                                           )
            for assign in request.data['assign_user']:
                try:
                    ex_user = TaskUser.objects.get(email__iexact=assign['email'])
                except ObjectDoesNotExist:
                    ex_user = None
                if ex_user.role == 3 or ex_user is None:
                    ag_obj = TaskAssignUser.objects.create(
                        user=ex_user,
                        user_email=assign['email'].lower(),
                        task=task_obj
                    )

            assign_user = TaskAssignUser.objects.filter(task=task_obj, active=Task)
            assign_serialiser = TaskAssignUserSerializer(assign_user, many=True)
            context = {
                'task': TaskSerializer(task_obj).data,
                'assign': assign_serialiser.data
            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def dashboard(self, request):
        user_perm = has_permission(request)
        if user_perm.role == 1:
            task_obj = Task.objects.filter(active=True)
            response_serializer = TaskSerializer(task_obj, many=True).data
        elif user_perm.role == 2:
            task_obj = Task.objects.filter(created_by=user_perm, active=True)
            response_serializer = TaskSerializer(task_obj, many=True).data
        else:
            task_obj = TaskAssignUser.objects.filter(
                user_email__iexact=user_perm.email, active=True
            )
            response_serializer = [
                {
                    'question': i.task.question,
                    'created_by': {
                        'id': i.task.created_by.id,
                        'email': i.task.created_by.email,
                        'role': i.task.created_by.role
                    },
                    'status': i.status
                }
                for i in task_obj
                ]
        return Response({'data': response_serializer, }, status=status.HTTP_200_OK)

    def task_delete(self, request, pk=None):
        user_perm = has_permission(request)
        if user_perm.role == 1:
            task_obj = get_object_or_404(Task, id=pk, active=True)
            task_obj.active = False
            task_obj.save()
            context = {'message': 'successful deleted '}
        else:
            context = {'message': 'not permission to delete'}

        return Response(context, status=status.HTTP_200_OK)

    def status_change(self, request, pk=None):
        user_perm = has_permission(request)
        assign_obj = get_object_or_404(TaskAssignUser, id=pk, active=True)
        if user_perm.role == (1 or 2):
            if assign_obj.status == 'done':
                assign_obj.status = request.data['status']
                assign_obj.save()
        else:
            if assign_obj.status == 'to-do':
                assign_obj.status = 'doing'
                assign_obj.save()
            elif assign_obj.status == 'doing':
                assign_obj.status = 'done'
                assign_obj.save()
        return Response({'message': 'status changes!'}, status=status.HTTP_200_OK)
