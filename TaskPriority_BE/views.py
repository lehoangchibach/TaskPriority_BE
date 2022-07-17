import imp
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

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
