import imp
import re
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from uuid import uuid4

from TaskPriority_BE.models import Users, Task, Tasks
from TaskPriority_BE.serializers import UsersSerializer, TaskSerializer, TasksSerializer


# Create your views here.


@csrf_exempt
def usersAPI(request, userName=' '):
    if request.method == 'GET':
        users = Users.objects.all()
        users_serializer = UsersSerializer(users, many=True)
        return JsonResponse(users_serializer.data, safe=False)

    if request.method == 'POST':
        user_data = JSONParser().parse(request)
        users_serializer = UsersSerializer(data=user_data)
        if users_serializer.is_valid():
            users_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)

    if request.method == 'PUT':
        user_data = JSONParser().parse(request)
        user = Users.objects.get(userName=user_data['userName'])
        users_serializer = UsersSerializer(user, data=user_data)
        if users_serializer.is_valid():
            users_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update", safe=False)

    if request.method == 'DELETE':
        user_data = Users.objects.get(userName=userName)
        user_data.delete()
        return JsonResponse("Deleted Successfully", safe=False)


@csrf_exempt
def taskAPI(request, taskId=' '):
    if request.method == 'GET':
        task = Task.objects.get(taskId=taskId)
        # task = Task.objects.all()
        task_serializer = TaskSerializer(task).data
        if not task_serializer:
            return JsonResponse('Can not find task', safe=False)
        return JsonResponse(task_serializer, safe=False)

    if request.method == 'POST':
        task = JSONParser().parse(request)
        task['taskId'] = uuid4().hex
        task_serializer = TaskSerializer(data=task)
        if task_serializer.is_valid():
            task_serializer.save()
            return JsonResponse('Added Successfully', safe=False)
        return JsonResponse("Failed to Add", safe=False)

    if request.method == 'PUT':
        taskChange = JSONParser().parse(request)
        taskCurrent = Task.objects.get(taskId=taskChange['taskId'])
        task_serializer = TaskSerializer(taskCurrent, data=taskChange)
        if task_serializer.is_valid():
            task_serializer.save()
            return JsonResponse('Updated Successfully', safe=False)
        return JsonResponse("Failed to Update", safe=False)

    if request.method == 'DELETE':
        task = Task.objects.get(taskId=taskId)
        task.delete()
        return JsonResponse("Deleted Successfully", safe=False)


@csrf_exempt
def addUserToTask(request, taskId=' ', userName=' '):
    if request.method == 'PUT':
        task = Task.objects.get(taskId=taskId)
        old_task = Task.objects.get(taskId=taskId)
        task_serializer = TaskSerializer(task).data
        task_serializer['owner'] = userName
        newtask_serializer = TaskSerializer(old_task, data=task_serializer)
        if newtask_serializer.is_valid():
            newtask_serializer.save()
            return JsonResponse('Added User Successfully', safe=False)
        return JsonResponse("Failed to Add User", safe=False)


@csrf_exempt
def getAllByUser(request, userName=' '):
    if request.method == 'GET':
        allTask = Task.objects.all()
        allTask_serializer = TaskSerializer(allTask, many=True).data
        allTask = list(filter(lambda each: each['owner'] ==
                              userName, allTask_serializer))
        taskGroup = {'low': [],
                     'normal': [],
                     'high': [],
                     'doing': [],
                     'done': [], }

        for task in allTask:
            taskGroup[task['priority']].append(task)
        return JsonResponse(taskGroup, safe=False)
