from datetime import datetime

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser
from django.db import IntegrityError
from todo.models import Todo
from .serializer import TodoSerializer, TodoCompleteSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.status import HTTP_204_NO_CONTENT


class TodoCompletedListAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):   # custom queryset
        todos = Todo.objects.filter(
            user=self.request.user, datecompleted__isnull=False
        ).order_by("-datecompleted")
        return todos


class TodoCreateAPIView(generics.CreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):  # custom saving obj
        serializer.save(user=self.request.user)


class TodoListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):   # update user before create (must be login user)
        serializer.save(user=self.request.user)

    def get_queryset(self):   # get user's todos (user related todos)
        return Todo.objects.filter(user=self.request.user)


class TodoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):   # get user's todos (user related todos)
        return Todo.objects.filter(user=self.request.user)

    def delete(self, *args, **kwargs):  # delete post
        todo = Todo.objects.get(pk=self.kwargs["pk"])
        if self.get_queryset().exists():
            self.destroy(self.request, *args, **kwargs)
            return Response({f'msg': f'Post "{todo}" was deleted'}, status=HTTP_204_NO_CONTENT)
        else:
            raise ValidationError(f'You never post for"{todo}')


class TodoCompleteRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoCompleteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):  # get user's todos (user related todos)
        todos = Todo.objects.filter(
            user=self.request.user, datecompleted__isnull=False
        ).order_by("-datecompleted")
        return todos

    def perform_update(self, serializer):  # update completedate while updating to current date time format
        serializer.instance.datecompleted = datetime.now()
        serializer.save()


@csrf_exempt
def signup(request):
    if request.method == "POST":
        try:
            data = JSONParser().parse(request)
            print(data, type(data))
            username = data.get('username')
            password = data.get('password')
            credentials = [username, password]
            if all(credentials):
                user = User.objects.create_user(
                    data["username"], password=data["password"]
                )
                user.save()
                token = Token.objects.create(user=user)  # create new token from user (DRF adds it to admin panel)
                return JsonResponse({'token': token.key}, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse({'error': 'missing username or password'})
        except IntegrityError:
            return JsonResponse({'error': 'username already token'})


@csrf_exempt
def apilogin(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        print(data, type(data))
        username = data.get('username')
        password = data.get('password')
        credentials = [username, password]
        if all(credentials):
            user = authenticate(request, username=username, password=password)
            if user:
                # find from user (DRF adds it to admin panel)
                token = Token.objects.filter(user=user).first()
                return JsonResponse({'token': token.key}, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse({'error': f'can not login "{username}"'})
        else:
            return JsonResponse({'error': 'missing username or password'})