'''Test module for todo_list app'''

from django.test import TestCase
from django.urls import reverse

from .models import TODO

def create_task(header=None, description=None, isDone=False):
    return TODO.objects.create(header=header, description=description, isDone=isDone)

class TestIndexPage(TestCase):
    '''Tests for index page'''
    def test_index_page_responding(self):
        '''Page must have 200 respose code'''
        resp = self.client.get(reverse('todo:index'))
        self.assertEquals(resp.status_code, 200)

    def test_no_items_in_todo_list(self):
        '''Page must show text if there is no tasks'''
        resp = self.client.get(reverse('todo:index'))
        self.assertContains(resp, 'You have no tasks yet')
        self.assertQuerysetEqual(resp.context['data'], [])

    def test_items_in_todo_list(self):
        '''Page must show tasks that is in progress'''
        task = create_task('New Task', 'There is new task here')
        resp = self.client.get(reverse('todo:index'))
        self.assertContains(resp, task.header)
        self.assertContains(resp, task.description)
        self.assertQuerysetEqual(resp.context['data'], ['<TODO: New Task>'])

    def test_display_only_not_done_tasks(self):
        '''Page must show only tasks that is not done'''
        create_task('First', 'First task', True)
        create_task('Second', 'Second task')
        resp = self.client.get(reverse('todo:index'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Second')
        self.assertNotContains(resp, 'First')
        self.assertQuerysetEqual(resp.context['data'], ['<TODO: Second>'])

    def test_display_multiple_tasks(self):
        '''If there is multiple tasks they show be on index page'''
        create_task('First', 'First task')
        create_task('Second', 'Second task')
        resp = self.client.get(reverse('todo:index'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'First task')
        self.assertContains(resp, 'Second task')
        self.assertQuerysetEqual(resp.context['data'],\
        ['<TODO: Second>', '<TODO: First>'], ordered=False)


class TestNewTaskPage(TestCase):
    def test_new_task_page_responding(self):
        resp = self.client.get(reverse('todo:new_task'))
        self.assertEqual(resp.status_code, 200)

    def test_csrf_token_presents(self):
        resp = self.client.get(reverse('todo:new_task'))
        self.assertContains(resp, 'csrfmiddlewaretoken')

    def test_form_raises_error_with_missing_data(self):
        resp = self.client.post(reverse('todo:new_task'), {}, follow=True)
        form = resp.context.get('form')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(form.errors)
        self.assertFormError(resp, 'form', 'header', 'This field is required.')

    def test_form_without_description_data(self):
        resp = self.client.post(reverse('todo:new_task'), {'header': "My New Task"}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertRedirects(resp, reverse('todo:index'))
        self.assertTrue(TODO.objects.exists())

    def test_form_creates_new_task_with_full_data(self):
        resp = self.client.post(reverse('todo:new_task'), \
            {'header':'My New Task', 'description':'This is my new task'}, follow=True)
        self.assertRedirects(resp, reverse('todo:index'))
        self.assertContains(resp, "My New Task")
        self.assertTrue(TODO.objects.exists())


class TestEditPage(TestCase):
    def setUp(self):
        create_task('Unique Task', 'First task')

    def test_edit_page_without_tasks_created(self):
        resp = self.client.get(reverse('todo:edit_task', kwargs={'pk': 2}))
        self.assertEqual(resp.status_code, 404)

    def test_csrf_token_presents(self):
        resp = self.client.get(reverse('todo:edit_task', kwargs={'pk': 1}))
        self.assertContains(resp, 'csrfmiddlewaretoken')

    def test_edit_page_with_tasks_created(self):
        resp = self.client.get(reverse('todo:edit_task', kwargs={'pk': 1}))
        form = resp.context.get('form')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Unique Task')
        self.assertContains(resp, 'First task')
        self.assertFalse(form.errors)

    def test_edit_task_in_wrong_way(self):
        resp = self.client.post(reverse('todo:edit_task', kwargs={'pk': 1}), {'header': ''})
        form = resp.context.get('form')
        self.assertEquals(resp.status_code, 200)
        self.assertTrue(form.errors)

    def test_edit_task_with_valid_data_redirects(self):
        resp = self.client.post(reverse('todo:edit_task', kwargs={'pk': 1}),
                                {'header': 'New Header'})
        self.assertRedirects(resp, reverse('todo:index'))

    def test_edit_task_with_valid_data_changes_data(self):
        data = {'header': 'New Header', 'description': 'New description'}
        resp = self.client.post(reverse('todo:edit_task', kwargs={'pk': 1}),
                                data, follow=True)
        self.assertContains(resp, 'New Header')
        self.assertContains(resp, 'New description')
        self.assertNotContains(resp, 'Unique Task')
        self.assertNotContains(resp, 'First task')


class TestDonePage(TestCase):
    def setUp(self):
        self.task = create_task("New task", "This task is new")

    def test_404_if_there_task_is_not_created(self):
        resp = self.client.post(reverse('todo:make_done', kwargs={'pk': 100}), {})
        self.assertEqual(resp.status_code, 404)

    def test_done_task_page_not_allowed_method(self):
        resp = self.client.get(reverse('todo:make_done', kwargs={'pk' : 1}))
        self.assertEqual(resp.status_code, 405)

    def test_done_task_showing_warning_if_task_already_done(self):
        self.task.isDone = True
        resp = self.client.post(reverse('todo:make_done', kwargs={'pk': 1}))
        self.assertRedirects(resp, reverse('todo:index'))
        resp = self.client.post(reverse('todo:make_done', kwargs={'pk': 1}), follow=True)
        msg = list(resp.context.get('messages'))[0]
        self.assertEqual(msg.message, 'The Task is already done.')
        self.assertEqual(msg.tags, 'warning')
        self.assertContains(resp, "The Task is already done.")

    def test_done_task_is_working(self):
        resp = self.client.post(reverse('todo:make_done', kwargs={'pk':1}))
        self.assertRedirects(resp, reverse('todo:index'))

    def test_done_is_working_after_redirect(self):
        resp = self.client.post(reverse('todo:make_done', kwargs={'pk':1}), follow=True)
        msg = list(resp.context.get('messages'))[0]
        self.assertEqual(msg.tags, 'success')
        self.assertEqual(msg.message, 'Task is now done.')
        self.assertContains(resp, "<strong>Congradulations!</strong> Task is now done.")

class TestDoneTasksList(TestCase):
    def setUp(self):
        self.url = reverse('todo:done_list')
        # create_task("My Done Task", "This task is created to be done", True)

    def test_done_task_list_responding(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)

    def test_done_list_without_tasks(self):
        resp = self.client.get(self.url)
        self.assertContains(resp, 'You have no done tasks')
        self.assertQuerysetEqual(resp.context['data'], [])

    def test_done_list_with_done_task(self):
        create_task('My done task', 'This task was created done', True)
        resp = self.client.get(self.url)
        self.assertContains(resp, 'My done task')
        self.assertContains(resp, 'This task was created done')
        self.assertQuerysetEqual(resp.context['data'], ['<TODO: My done task>'])

    def test_done_list_with_multiple_done_tasks(self):
        create_task('My first done task', 'This task was created done first', True)
        create_task('My second done task', 'This task was created done second', True)
        resp = self.client.get(self.url)
        self.assertContains(resp, 'My first done task')
        self.assertContains(resp, 'This task was created done first')
        self.assertContains(resp, 'My second done task')
        self.assertContains(resp, 'This task was created done second')
        self.assertQuerysetEqual(resp.context['data'],
                                 ['<TODO: My first done task>',
                                  '<TODO: My second done task>'], ordered=False)

    def test_done_with_done_and_tasks_in_progress(self):
        task_done = create_task('My done task', 'This task is created done', True)
        task_in_progress = create_task('My task in progress', 'This task is created in progress')
        resp = self.client.get(self.url)
        self.assertContains(resp, task_done.header)
        self.assertContains(resp, task_done.description)
        self.assertNotContains(resp, task_in_progress.header)
        self.assertNotContains(resp, task_in_progress.description)
        self.assertQuerysetEqual(resp.context['data'], ['<TODO: My done task>'])

class TestTaskInProgressView(TestCase):
    def setUp(self):
        self.task = create_task('Task', 'This is test task for tests')
        self.task_done = create_task('Done task', 'This task was created done', True)
        self.url = reverse('todo:make_in_progress', kwargs={'pk': self.task.pk})
        self.url_done = reverse('todo:make_in_progress', kwargs={'pk':self.task_done.pk})

    def test_task_is_not_exists(self):
        resp = self.client.post(reverse('todo:make_in_progress', kwargs={'pk':100}), follow=True)
        self.assertEqual(resp.status_code, 404)

    def test_make_in_progress_not_allowed_method(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 405)

    def test_task_is_not_done(self):
        resp = self.client.post(self.url, follow=True)
        msg = list(resp.context.get('messages'))[0]
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'The Task is not done yet.')
        self.assertEqual(msg.message, 'The Task is not done yet.')
        self.assertEqual(msg.tags, 'warning')

    def test_done_task_becomes_in_progress(self):
        self.task.isDone = True
        resp = self.client.post(self.url_done, follow=True)
        msg = list(resp.context.get('messages'))[0]
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'The task is In Progress again.')
        self.assertEqual(msg.tags, 'success')
        self.assertEqual(msg.message, 'The task is In Progress again.')
