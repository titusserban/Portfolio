from django.shortcuts import render
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Task
from django.views import View
from django.shortcuts import redirect
from django.db import transaction
from .forms import TaskForm


class TaskList(ListView):
    model = Task
    context_object_name = 'tasks'
    def get_context_data(self, **kwargs):
        context = super(TaskList, self).get_context_data(**kwargs)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)

        context['search_input'] = search_input

        return context


class TaskDetail(DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'to_do_app/task.html'


class TaskCreate(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'to_do_app/task_form.html'

    def get_form_kwargs(self):
        kwargs = super(TaskCreate, self).get_form_kwargs()
        kwargs.update({"pk": None})
        return kwargs

    def get_success_url(self):
        return reverse('to_do_app:tasks')


class TaskUpdate(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'to_do_app/task_form.html'
    
    def get_form_kwargs(self):
        kwargs = super(TaskUpdate, self).get_form_kwargs()
        kwargs.update({"pk": self.kwargs["pk"]})
        return kwargs

    def form_valid(self, form):
        return super(TaskUpdate, self).form_valid(form)

    def form_invalid(self, form):
        return super(TaskUpdate, self).form_invalid(form)

    def get_success_url(self):
        return reverse('to_do_app:tasks')  


class TaskDelete(DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('to_do_app:tasks')    


class TaskReorder(View):
    def post(self, request):
        form = TaskForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('to_do_app:tasks'))