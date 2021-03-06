from django.urls import path
from .views import TodoCompletedListAPIView, TodoCreateAPIView, \
    TodoListCreateAPIView, TodoRetrieveUpdateDestroyAPIView, TodoCompleteRetrieveUpdateDestroyAPIView, signup, apilogin


urlpatterns = [
    # API
    path("todo/completed/<pk>/", TodoCompletedListAPIView.as_view(), name='todo_complete_lis_APIView'),
    path("todos/", TodoCreateAPIView.as_view(), name='todo_createAPIView'),
    path("todos_list_create/", TodoListCreateAPIView.as_view(), name='todos_list_create'),
    path("todo_retrieve_update_destroy/<pk>/", TodoRetrieveUpdateDestroyAPIView.as_view(),
         name='todo_retrieve_update_destroy'),
    path("todo/complete/<pk>/", TodoCompleteRetrieveUpdateDestroyAPIView.as_view(),
         name='Todo_complete'),

    path('signup/', signup, name='signup'),
    path('login/', apilogin, name='apilogin')
]
