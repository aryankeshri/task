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
        if user_perm.role == 1 or user_perm.role == 2:
            task_obj = Task.objects.create(question=request.data['question'],
                                           created_by=user_perm
                                           )
            for assign in request.data['assign_user']:
                try:
                    ex_user = TaskUser.objects.get(email__iexact=assign['email'])
                except ObjectDoesNotExist:
                    ex_user = None
                ag_obj = TaskAssignUser.objects.create(
                    user=ex_user,
                    user_email=assign['email'].lower(),
                    task=task_obj
                )

            assign_user = TaskAssignUser.objects.filter(task=task_obj, active=True)
            assign_serialiser = TaskAssignUserSerializer(assign_user, many=True)
            context = {
                'task': TaskSerializer(task_obj).data,
                'assign': assign_serialiser.data
            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def update_task(self, request, pk=None):
        """
        Update task method
        :param request:
            header = jwt token
            data = {
                question: 'abcd ?',
                remove_assign_users: [1,2,3]
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
        task_obj = get_object_or_404(Task, id=pk, active=True)
        if user_perm.role == 1 or task_obj.created_by.id == user_perm.id:
            task_obj.question = request.data['question']
            task_obj.save()
            for remove_assign_user in request.data['remove_assign_users']:
                goal = get_object_or_404(TaskAssignUser, id=remove_assign_user, task=pk)
                goal.active = False
                goal.save()
            for assign in request.data['assign_user']:
                try:
                    ex_user = TaskUser.objects.get(email__iexact=assign['email'])
                except ObjectDoesNotExist:
                    ex_user = None
                ag_obj = TaskAssignUser.objects.create(
                    user=ex_user,
                    user_email=assign['email'].lower(),
                    task=task_obj,
                    status=assign['status']
                )
            assign_user = TaskAssignUser.objects.filter(task=task_obj, active=True)
            assign_serialiser = TaskAssignUserSerializer(assign_user, many=True)
            context = {
                'task': TaskSerializer(task_obj).data,
                'assign': assign_serialiser.data
            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def dashboard(self, request):
        """

        :param request: request according to user type
        :return: {
            "data": [
                {
                    "question": "How was add two no?",
                    "status": "to-do",
                    "created_by": {
                        "role": 2,
                        "id": 7,
                        "email": "teacher1@gmail.com"
                    }
                },
                {
                    "question": "How was add two no?",
                    "status": "to-do",
                    "created_by": {
                        "role": 2,
                        "id": 7,
                        "email": "teacher1@gmail.com"
                    }
                }
            ]
        }
        """
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
        if user_perm.role == 1 or user_perm.role == 2:
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

    def task_details(self, request, pk=None):
        user_perm = has_permission(request)
        task_obj = get_object_or_404(Task, id=pk, active=True)
        task_response = TaskSerializer(task_obj)
        assign_objs = TaskAssignUser.objects.filter(task=task_obj, active=True)
        assign_response = TaskAssignUserSerializer(assign_objs, many=True)
        context = {
            'task': task_response.data,
            'assign': assign_response.data
        }
        return Response(context, status=status.HTTP_200_OK)
