from django.urls import path
from .views import *

app_name = 'projectapp'

urlpatterns=[
    path('list/', ListProjectView.as_view(), name='list'),
    path('create/', CreateProjectView.as_view(), name='create'),
    path('detail/<int:pk>', DetailProjectView.as_view(), name='detail'),
]