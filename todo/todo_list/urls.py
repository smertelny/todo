from django.conf.urls import url

from .views import index

app_name = 'todo'
urlpatterns = [
    url(r'^$', index, name='index'),
]