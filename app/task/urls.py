from django.urls import path

from task.views import TaskListView, TaskActionsView, TaskCreateView

urlpatterns = [
    path("list/", TaskListView.as_view(), name="task_list"),
    path('<str:action>/<int:task_id>/', TaskActionsView.as_view(), name='task_action'),
    path('create/', TaskCreateView.as_view(), name='create_task'),
]