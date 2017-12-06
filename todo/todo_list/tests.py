from django.test import TestCase
from django.urls import reverse

from .models import TODO

def create_task(header=None, description=None, isDone=False):
    return TODO.objects.create(header=header, description=description, isDone=isDone)

class TestIndexPage(TestCase):
    def test_index_page_responding(self):
        resp = self.client.get(reverse('todo:index'))
        self.assertEquals(resp.status_code, 200)

    def test_no_items_in_todo_list(self):
        resp = self.client.get(reverse('todo:index'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'You have no tasks yet')
        self.assertQuerysetEqual(resp.context['data'], [])

    def test_items_in_todo_list(self):
        create_task('New Task', 'There is new task here')
        resp = self.client.get(reverse('todo:index'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'New Task')
        self.assertQuerysetEqual(resp.context['data'], ['<TODO: New Task>'])

    def test_display_only_not_done_tasks(self):
        create_task('First', 'First task', True)
        create_task('Second', 'Second task')
        resp = self.client.get(reverse('todo:index'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Second')
        self.assertNotContains(resp, 'First')
        self.assertQuerysetEqual(resp.context['data'], ['<TODO: Second>'])

    def test_display_multiple_tasks(self):
        create_task('First', 'First task')
        create_task('Second', 'Second task')
        resp = self.client.get(reverse('todo:index'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'First task')
        self.assertContains(resp, 'Second task')
        self.assertQuerysetEqual(resp.context['data'],\
        ['<TODO: Second>', '<TODO: First>'], ordered=False)


class TestEditPage(TestCase):
    def test_edit_page_without_tasks_created(self):
        resp = self.client.get(reverse('todo:edit_task', kwargs={'pk': 1}))
        self.assertEqual(resp.status_code, 404)

    def test_edit_page_with_tasks_created(self):
        create_task('Task', 'First task')
        resp = self.client.get(reverse('todo:edit_task', kwargs={'pk': 1}))
        form = resp.context.get('form')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Task')
        self.assertContains(resp, 'First task')
        self.assertFalse(form.errors)

    def test_edit_data_in_wrong_way(self):
        create_task('Task', 'First task')
        resp = self.client.post(reverse('todo:edit_task', kwargs={'pk': 1}), {'header': ''})
        
        print(resp.context)
        