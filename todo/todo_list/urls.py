from django.conf.urls import url

from .views import index, new_task

app_name = 'todo'
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^new/$', new_task, name='new_task'),
]