from django.conf.urls import url

from . import views

app_name = 'todo'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new$', views.new_task, name='new_task'),
    url(r'^edit/(?P<pk>\d+)$', views.edit, name='edit_task'),
    url(r'^done-list', views.done_tasks_list, name='done_list'),
    url(r'^done/(?P<pk>\d+)$', views.make_task_done, name='make_done'),
    url(r'^make_in_progress/(?P<pk>\d+)$', views.make_task_in_progress, name='make_in_progress'),
]
