from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from .views import ToDoViewSet

router = DefaultRouter()
router.register(r'todo', ToDoViewSet)

urlpatterns = [
    url(r'^v1/', include(router.urls)),
]
