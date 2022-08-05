from django.urls import path
from TaskPriority_BE import views

urlpatterns = [
    path('user/', views.usersAPI),
    # path('user/<str:userName>', views.usersAPI),

    path('user/createUser', views.createUser),
    path('user/logIn', views.logIn),
    path('user/changePassword', views.changePassword),
    path('user/updateDisplayName', views.updateDisplayName),

    path('task/', views.taskAPI),
    path('task/<str:taskId>', views.taskAPI),

    path('task/addUserToTask/<str:taskId>%<str:userName>', views.addUserToTask),

    path('task/getAllByUser/<str:userName>', views.getAllByUser)

]
