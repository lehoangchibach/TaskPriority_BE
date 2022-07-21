from rest_framework import serializers
from TaskPriority_BE.models import Users, Task, Tasks


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('userName', 'displayName', 'password')


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('owner', 'taskId', 'title', 'summary', 'detail',
                  'deadlineTime', 'deadlineDate', 'priority')
        # fields = ('taskId', 'title', 'summary', 'detail',
        #           'deadlineTime', 'deadlineDate', 'priority')
        # fields = ('taskId', 'title', 'summary', 'priority')


class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ('owner', 'low', 'normal', 'high',
                  'doing', 'done')
