from django.urls import path
from TaskPriority_BE import views

urlpatterns = [
    path('user/', views.usersAPI),
    path('user/<str:userName>', views.usersAPI)
]
