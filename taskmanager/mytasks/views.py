from django.shortcuts import render
from mytasks.models import Task
from rest_framework.response import Response
from rest_framework import status
from mytasks.serializers import TaskSerializer, UserSerializer, LoginSerializer
from rest_framework.views import APIView
from rest_framework import permissions
from mytasks.permissions import IsOwnerOrReadOnly
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.http import Http404


# Create your views here.
class RegisterUser(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data["password1"])
            user.save()

            auth_user = authenticate(
                request, username=user.username, password=request.data["password1"]
            )

            if auth_user is not None:
                login(request, auth_user)
                token, created = Token.objects.get_or_create(user=auth_user)

                return Response(
                    {
                        "message": "Registration successful",
                        "user": serializer.data,
                        "token": token.key,
                    },
                    status=status.HTTP_201_CREATED,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUser(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            auth_user = authenticate(
                request,
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"],
            )
            if auth_user is not None:
                login(request, auth_user)
                token, created = Token.objects.get_or_create(user=auth_user)
                return Response(
                    {"message": "Login successful", "token": token.key},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "Invalid username or password"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            request.auth.delete()
            logout(request)
            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        except AttributeError:
            return Response(
                {"message": "User not logged in"}, status=status.HTTP_400_BAD_REQUEST
            )


class TaskList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        status_filter = request.query_params.get("status")
        tasks = Task.objects.all().order_by("due_date")

        if status_filter:
            tasks = Task.objects.filter(is_completed=status_filter)

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(added_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        task = self.get_object(pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        task = self.get_object(pk)
        self.check_object_permissions(request, task)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = self.get_object(pk)
        task.delete()
        return Response(
            {"message": "Task deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )
