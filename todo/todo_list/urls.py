from django.conf.urls import url

from .views import index, new_task, make_task_done

app_name = 'todo'
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^new/$', new_task, name='new_task'),
    url(r'^done/(?P<pk>\d+)$', make_task_done, name='make_done'),
]