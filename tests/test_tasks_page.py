from flask import url_for
from . import BaseTest, dbsession as s
from raiden.models import Task


class TasksPageTest(BaseTest):
    def test_render_correct_template(self):
        resp = self.client.get(url_for('tasks'))
        self.assertTemplateUsed('tasks.html')
