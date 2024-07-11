from rest_framework.response import Response
from rest_framework import status, viewsets, generics
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from . import serializers
from .serializers import *

# M A N U A L L Y   G E N E R A T E   T O K E N
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Registration Successful!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogInView(APIView):
    def post(self, request, format=None):
        serializer = UserLogInSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.data.get('username')
            password = serializer.data.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response(
                    {
                        'token': token,
                        'msg': 'Login Successful!'
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response({'errors': {'non_field_errors': ['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class UserDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #permission_classes = [IsAuthenticated]
    lookup_field = 'id'

class ProjectListView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    #permission_classes = [IsAuthenticated]

class ProjectDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    #permission_classes = [IsAuthenticated]
    lookup_field = 'id'

class TaskListView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    #permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return Task.objects.filter(project_id=project_id)

    def perform_create(self, serializer):
        project_id = self.kwargs['project_id']
        project = get_object_or_404(Project, pk=project_id)
        serializer.save(project=project)

class TaskDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    #permission_classes = [IsAuthenticated]
    lookup_field = 'id'

class CommentListView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    #permission_classes = [IsAuthenticated]

    def get_queryset(self):
        task_id = self.kwargs['task_id']
        return Comment.objects.filter(task_id=task_id)

    def perform_create(self, serializer):
        task_id = self.kwargs['task_id']
        task = get_object_or_404(Task, pk=task_id)
        serializer.save(task=task)

class CommentDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    #permission_classes = [IsAuthenticated]
    lookup_field = 'id'
