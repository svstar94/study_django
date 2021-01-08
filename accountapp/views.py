from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .decorators import account_ownership_required

has_ownership = [login_required, account_ownership_required]

from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class AccountCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'accountapp/create.html'
    def get_success_url(self):
        return reverse_lazy('accountapp:login')

from django.views.generic.list import MultipleObjectMixin
class AccountDetailView(DetailView, MultipleObjectMixin):
    model = User
    context_object_name = 'target_user'
    template_name = 'accountapp/detail.html'

    paginate_by = 25

    def get_context_data(self, **kwargs):
        object_list = Article.objects.filter(writer=self.get_object())
        return super(AccountDetailView, self).get_context_data(object_list=object_list, **kwargs)

from .forms import AccountUpdateForm
from articleapp.models import Article

@method_decorator(has_ownership, 'get')
@method_decorator(has_ownership, 'post')
class AccountUpdateView(UpdateView):
    model = User
    form_class = AccountUpdateForm
    context_object_name = 'target_user'
    template_name = 'accountapp/update.html'

    def get_success_url(self):
        return reverse_lazy('accountapp:login', kwargs={'pk':self.object.pk})

@method_decorator(has_ownership, 'get')
@method_decorator(has_ownership, 'post')
class AccountDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('accountapp:login')
    context_object_name = 'target_user'
    template_name = 'accountapp/delete.html'
