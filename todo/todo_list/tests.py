from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import TODO

class TestIndexPage(TestCase):
    def test_index_page_responding(self):
        resp = self.client.get(reverse('todo:index'))
        self.assertEquals(resp.status_code, 200)

    def test_no_items_in_todo_list(self):
        resp = self.client.get(reverse('todo:index'))
        self.assertContains(resp, 'There is no data here')

    def test_items_in_todo_list(self):
        TODO.objects.create(
            header='New Task',
            description='There is new task here'
            )
        resp = self.client.get(reverse('todo:index'))
        self.assertContains(resp, 'New Task')
    
    def test_display_only_not_done_tasks(self):
        TODO.objects.create(
            header='First',
            description='First task',
            isDone=True
        )
        TODO.objects.create(
            header='Second',
            description='Second task',
        )
        resp = self.client.get(reverse('todo:index'))
        self.assertContains(resp, 'Second')
        self.assertNotContains(resp, 'First')

