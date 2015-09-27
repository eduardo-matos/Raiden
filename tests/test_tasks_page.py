from flask import url_for
from . import BaseTest, dbsession as s
from raiden.models import Task


class TasksPageTest(BaseTest):
    def setUp(self):
        self.task_1 = Task(title='Ham', item_count=10, current_count=4, slug='d41d8cd98f00b204e9800998ecf8427e')
        self.task_2 = Task(title='Spam', item_count=10, current_count=7, slug='e09f6a7593f8ae3994ea57e1117f67ec')
        s.add_all([self.task_1, self.task_2])
        s.commit()

    def test_show_current_tasks_slug(self):
        content = self.client.get(url_for('tasks')).data.decode('utf-8')

        self.assertIn(self.task_1.slug, content)
        self.assertIn(self.task_2.slug, content)

    def test_show_current_tasks_percentages(self):
        content = self.client.get(url_for('tasks')).data.decode('utf-8')

        self.assertIn('40%', content)
        self.assertIn('70%', content)
