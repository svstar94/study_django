from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from .models import Project
from .forms import ProjectCreationForm
from django.urls import reverse, reverse_lazy

from .decorators import project_ownership_required

# Create your views here.

@method_decorator(login_required, 'get')
@method_decorator(login_required, 'post')
class CreateProjectView(CreateView):
    model = Project
    form_class = ProjectCreationForm
    template_name = 'projectapp/create.html'

    def form_valid(self, form):
        temp_project=form.save(commit=False)
        temp_project.writer = self.request.user
        temp_project.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('projectapp:detail', kwargs={'pk':self.object.pk})


from django.views.generic.list import MultipleObjectMixin
from articleapp.models import Article
from subscribeapp.models import Subscription
class DetailProjectView(DetailView, MultipleObjectMixin):
    model = Project
    context_object_name = 'target_project'
    template_name='projectapp/detail.html'

    paginated_by = 25

    def get_context_data(self, **kwargs):

        project = self.object
        user = self.request.user

        if user.is_authenticated:
            subscription = Subscription.objects.filter(user=user, project=project)
        else:
            subscription = None

        object_list = Article.objects.filter(project=self.get_object())
        return super(DetailProjectView, self).get_context_data(object_list=object_list, 
                                                                subscription=subscription,
                                                                **kwargs)

class ListProjectView(ListView):
    model = Project
    context_object_name = 'project_list'
    template_name = 'projectapp/list.html'
    paginate_by = 25
