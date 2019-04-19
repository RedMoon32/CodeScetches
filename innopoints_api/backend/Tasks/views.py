from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from Tasks.serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from .models import Task
from profile.models import UserProfile
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.parsers import JSONParser


class CanAlterTask(permissions.BasePermission):
    message = 'Not allowed'

    """
    Only user who created some task can edit it and its applications"
    """

    def has_permission(self, request, view):
        user = get_object_or_404(UserProfile.objects.filter(user=request.user))
        id = request.query_params['id'] if request.method == 'GET' else request.data['id']
        task = get_object_or_404(Task.objects.filter(id=id))
        return task.owner == user


class CanAlterApplication(permissions.BasePermission):
    message = 'Not allowed'

    """
       Only user who created some task can edit it and its applications"
    """

    def has_permission(self, request, view):
        user = get_object_or_404(UserProfile.objects.filter(user=request.user))
        id = request.query_params['id'] if request.method == 'GET' else request.data['id']
        app = get_object_or_404(Application.objects.filter(id=id))
        return app.task.owner == user


class CreatedTasks(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TaskSerializer

    """Get all tasks which user created"""

    def get_queryset(self):
        user = get_object_or_404(UserProfile.objects.filter(user=self.request.user))
        return Task.objects.filter(owner=user)


class GetTaskApplications(ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = (CanAlterTask, IsAuthenticated)

    """Get applications for this task(only for creator of tasks), {id: 0}"""

    def get_queryset(self):
        task = get_object_or_404(Task.objects.filter(id=self.request.query_params['id']))
        app = Application.objects.filter(task=task)
        return app


class GetUserApplications(ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = (IsAuthenticated,)

    """Get all tasks where user has applied"""

    def get_queryset(self):
        user = get_object_or_404(UserProfile.objects.filter(user=self.request.user))
        app = Application.objects.filter(volunteer=user)
        return app


class CreateTask(CreateAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    """Create new task"""

    def perform_create(self, serializer):
        serializer.save(owner=UserProfile.objects.get(user=self.request.user))


class GetAllTasks(ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class UpdateTask(UpdateAPIView):
    permission_classes = (CanAlterTask, IsAuthenticated)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_object(self):
        return get_object_or_404(Task.objects.filter(id=self.request.data['id']))


class ApplyForTask(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        task = get_object_or_404(Task.objects.filter(pk=request.data['id']))
        if task.is_active and (task.owner is None or task.owner.user != request.user):
            user = UserProfile.objects.get(user=request.user)
            if not Application.objects.filter(volunteer=user, task=task).exists():
                app = Application.objects.create(volunteer=user, task=task)
                return Response(data=ApplicationSerializer(app).data, status=status.HTTP_200_OK)
            else:
                return Response('error', status=status.HTTP_409_CONFLICT)
        else:
            return Response('error', status=status.HTTP_400_BAD_REQUEST)


class UpdateApplicationStatus(APIView):
    permission_classes = (CanAlterApplication, IsAuthenticated)

    @staticmethod
    def post(request):
        app = get_object_or_404(Application.objects.filter(pk=request.data['id']))
        new_status = request.data['status']
        if new_status not in [Application.DCL, Application.ACP, Application.FNS, ]:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            if new_status == Application.FNS:
                if (app.status == Application.ACP or app.status == Application.FNS) and request.data[
                    'inno_points'] <= app.task.inno_points:
                    app.inno_points = app.xp_points = request.data['inno_points']
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            if new_status == Application.DCL and app.status != Application.PND:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            app.status = new_status
            app.save()
            return Response('OK', status=status.HTTP_200_OK)


class CancelApplication(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def delete(request):
        app = get_object_or_404(Application.objects.filter(pk=request.data['id']))
        user = get_object_or_404(UserProfile.objects.filter(user=request.user))
        if app.volunteer == user:
            if app.status not in [Application.CNC, Application.FNS, Application.DCL, Application.ACP]:
                app.status = Application.CNC
                app.save()
                return Response('OK', status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CloseTask(APIView):
    permission_classes = (CanAlterTask, IsAuthenticated)

    @staticmethod
    def delete(requst):
        task = get_object_or_404(Task.objects.filter(pk=requst.data['id']))
        if not task.awarded:
            task.save()
            for app in Application.objects.filter(task=task, status=Application.ACP):
                app.status = Application.FNS
                app.inno_points = app.xp_points = task.inno_points
                app.save()
            for app in Application.objects.filter(task=task, status=Application.PND):
                app.status = Application.CNC
                app.save()
            task.awarded = True
            task.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
