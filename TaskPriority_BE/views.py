from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from uuid import uuid4
import datetime

from TaskPriority_BE.models import Users, Task
from TaskPriority_BE.serializers import UsersSerializer, TaskSerializer


# Create your views here.


@csrf_exempt
def usersAPI(request, userName=' '):
    if request.method == 'GET':
        users = Users.objects.all()
        users_serializer = UsersSerializer(users, many=True)
        return JsonResponse(users_serializer.data, safe=False)

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
def createUser(request):
    if (request.method == 'POST'):
        user_data = JSONParser().parse(request)

        user = None
        users = UsersSerializer(Users.objects.all(), many=True).data
        for each in users:
            if each['userName'] == user_data['userName']:
                user = each
                break

        if (user):
            return JsonResponse("Username has already existed!", safe=False)

        user_serializer = UsersSerializer(data=user_data)
        if (user_serializer.is_valid()):
            user_serializer.save()
            return JsonResponse({"userName": user_data['userName'],
                                 "displayName": user_data['displayName']
                                 }, safe=False)
        return JsonResponse("Failed to create new user!", safe=False)


@csrf_exempt
def deleteUser(request):
    if (request.method == 'DELETE'):
        user_data = JSONParser().parse(request)
        user = Users.objects.get(userName=user_data['userName'])

        user.delete()
        return JsonResponse("Deleted Successfully", safe=False)


@csrf_exempt
def logIn(request):
    if (request.method == 'POST'):
        user_data = JSONParser().parse(request)

        user = None
        users = UsersSerializer(Users.objects.all(), many=True).data
        for each in users:
            if each['userName'] == user_data['userName']:
                user = each
                break

        if (not user):
            return JsonResponse("User not found!", safe=False)
        if (user_data['password'] != user['password']):
            return JsonResponse("Password is not correct!", safe=False)

        return JsonResponse({"userName": user['userName'],
                             "displayName": user['displayName']
                             }, safe=False)


@csrf_exempt
def changePassword(request):
    if (request.method == 'PUT'):
        user_data = JSONParser().parse(request)

        user = None
        users = UsersSerializer(Users.objects.all(), many=True).data
        for each in users:
            if each['userName'] == user_data['userName']:
                user = each
                oldUser = Users.objects.get(userName=user_data['userName'])
                break

        if (not user):
            return JsonResponse("User not found!", safe=False)

        if (user_data['oldPassword'] != user['password']):
            return JsonResponse("Old password is not correct!", safe=False)

        user['password'] = user_data['newPassword']
        user_serializer = UsersSerializer(oldUser, data=user)

        if (user_serializer.is_valid()):
            user_serializer.save()
            return JsonResponse("User updated successfully!", safe=False)
        return JsonResponse("Failed to update user!", safe=False)


@csrf_exempt
def updateDisplayName(request):
    if (request.method == 'PUT'):

        user_data = JSONParser().parse(request)

        user = None
        users = UsersSerializer(Users.objects.all(), many=True).data
        for each in users:
            if each['userName'] == user_data['userName']:
                user = each
                oldUser = Users.objects.get(userName=user_data['userName'])
                break

        if (not user):
            return JsonResponse("User not found!", safe=False)

        user['displayName'] = user_data['displayName']
        user_serializer = UsersSerializer(oldUser, data=user)

        if (user_serializer.is_valid()):
            user_serializer.save()
            return JsonResponse("User updated successfully!", safe=False)
        return JsonResponse("Failed to update user!", safe=False)


@csrf_exempt
def taskAPI(request, taskId=' '):
    if request.method == 'GET':
        task = Task.objects.get(taskId=taskId)
        task_serializer = TaskSerializer(task).data
        if not task_serializer:
            return JsonResponse('Can not find task', safe=False)
        return JsonResponse(task_serializer, safe=False)

    if request.method == 'POST':
        task = JSONParser().parse(request)
        task['taskId'] = uuid4().hex

        if (task['deadlineTime']):
            date_time_obj = datetime.datetime.strptime(
                task['deadlineTime'], '%Y-%m-%dT%H:%M:%S.%fZ')
            task['deadlineTime'] = date_time_obj.timetz()

        if (task['deadlineDate']):
            date_time_obj = datetime.datetime.strptime(
                task['deadlineDate'], '%Y-%m-%dT%H:%M:%S.%fZ')
            task['deadlineDate'] = date_time_obj.date()

        task_serializer = TaskSerializer(data=task)
        if task_serializer.is_valid():
            task_serializer.save()
            return JsonResponse('Added Successfully', safe=False)
        return JsonResponse("Failed to Add", safe=False)

    if request.method == 'PUT':
        taskChange = JSONParser().parse(request)
        taskCurrent = Task.objects.get(taskId=taskChange['taskId'])

        if (taskChange['deadlineTime']):
            date_time_obj = datetime.datetime.strptime(
                taskChange['deadlineTime'], '%Y-%m-%dT%H:%M:%S.%fZ')
            taskChange['deadlineTime'] = date_time_obj.timetz()

        if (taskChange['deadlineDate']):
            date_time_obj = datetime.datetime.strptime(
                taskChange['deadlineDate'], '%Y-%m-%dT%H:%M:%S.%fZ')
            taskChange['deadlineDate'] = date_time_obj.date()

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
