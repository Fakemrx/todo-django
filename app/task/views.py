from datetime import datetime, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, CreateView

from task.forms import TaskForm
from task.models import TaskModel


def home(request):
    return render(request, 'task/home.html')


class TaskListView(LoginRequiredMixin, ListView):
    model = TaskModel
    login_url = '/account/login/'
    template_name = 'task/list.html'

    def get_queryset(self):
        qs = TaskModel.objects.filter(user=self.request.user.pk).order_by('-created_at')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()

        for task in context.get('object_list'):
            if task.scheduled_at < now:
                task.remaining_time = None
                if not task.is_complete:
                    task.status = 'danger'
                continue

            remaining_time = task.scheduled_at - now
            total_seconds = remaining_time.total_seconds()

            if total_seconds < 3600 and not task.is_complete:
                task.status = 'warning'
            else:
                task.status = 'dark'

            total_seconds_without_ms = total_seconds - (total_seconds % 1)
            td_without_ms = timedelta(seconds=total_seconds_without_ms)
            task.remaining_time = td_without_ms
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = TaskModel
    login_url = '/account/login/'
    form_class = TaskForm
    template_name = 'task/create.html'
    success_url = '/task/list/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskActionsView(LoginRequiredMixin, View):
    login_url = '/account/login/'

    def post(self, request, action, task_id):
        task = get_object_or_404(TaskModel, pk=task_id)
        if not task.user == request.user:
            return redirect('/task/list/')
        if action == 'complete':
            if task.is_complete:
                task.is_complete = False
            else:
                task.is_complete = True
            task.save()
        elif action == 'delete':
            task.delete()
        return redirect('/task/list/')
