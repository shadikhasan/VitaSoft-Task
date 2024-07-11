from django.urls import path
from .views import *

urlpatterns = [
    path('api/users/register/', UserRegistrationView.as_view(), name='register'),
    path('api/users/login/', UserLogInView.as_view(), name='login'),
    path('api/users/<int:id>/', UserDetailsView.as_view(), name='user-detail'),
    path('api/projects/', ProjectListView.as_view(), name='project-list'),
    path('api/projects/<int:id>/', ProjectDetailsView.as_view(), name='project-detail'),
    path('api/projects/<int:project_id>/tasks/', TaskListView.as_view(), name='task-list'),
    path('api/tasks/<int:id>/', TaskDetailsView.as_view(), name='task-detail'),
    path('api/tasks/<int:task_id>/comments/', CommentListView.as_view(), name='comment-list'),
    path('api/comments/<int:id>/', CommentDetailsView.as_view(), name='comment-detail'),
]
