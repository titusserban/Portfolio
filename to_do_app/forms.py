from django.forms import ModelForm
from .models import Task

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title',
                  'description',
                  'complete',]

    def __init__(self, pk, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.pk = pk
