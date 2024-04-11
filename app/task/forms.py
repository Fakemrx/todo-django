import datetime

from django import forms

from task.models import TaskModel


class TaskForm(forms.ModelForm):
    title = forms.CharField(label='Title', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Insert title here',
    }))
    description = forms.CharField(required=False, label='Description', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Insert description here',
    }))
    scheduled_at = forms.DateTimeField(label='Date & Time', widget=forms.DateTimeInput(attrs={
        'class': 'form-control',
        'type': 'datetime-local',
        'placeholder': 'When it`s meant to be complete',
    }))

    class Meta:
        model = TaskModel
        fields = ('title', 'description', 'scheduled_at')

    def clean(self, *args, **kwargs):
        scheduled_at = self.cleaned_data.get('scheduled_at')
        now = datetime.datetime.now()
        print(f'Now:{now}, Scheduled: {scheduled_at}, ============ for debugging')
        if scheduled_at:
            if scheduled_at.date() < now.date():
                raise forms.ValidationError('Completion date cannot be before today')
            elif scheduled_at.date() == now.date():
                if scheduled_at.time() < now.time():
                    raise forms.ValidationError('Completion time cannot be before now')
        return super().clean(*args, **kwargs)
