from rest_framework import serializers
from .models import Task, Application


class ApplicationSerializer(serializers.ModelSerializer):
    volunteer = serializers.CharField(source='volunteer.user.email')

    class Meta:
        model = Application
        fields = ('id', 'volunteer', 'task', 'status', 'inno_points')


class TaskSerializer(serializers.ModelSerializer):
    applications = serializers.SerializerMethodField()

    # for user - see their applications
    # for admins - see applications for their task

    def get_applications(self, task):
        request = self.context['request']
        if request.user == task.owner.user:
            apps = Application.objects.filter(task=task)
            return ApplicationSerializer(apps, many=True, ).data
        else:
            apps = Application.objects.filter(task=task, volunteer__user=request.user)
            return ApplicationSerializer(apps, many=True, ).data

    class Meta:
        model = Task
        fields = (
            'id', 'title', 'description', 'inno_points', 'event_time', 'applications', 'event_time',)
