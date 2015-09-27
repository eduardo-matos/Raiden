from flask import url_for
from . import BaseTest, dbsession as s
from raiden.models import Task


class RetrieveTasksTest(BaseTest):
    def test_returns_all_tasks(self):
        s.add_all([Task(title='ham', slug='spam', item_count=10, current_count=2),
                   Task(title='egg', slug='jam', item_count=5, current_count=3)])

        resp = self.client.get(url_for('api_tasks'))

        self.assertEquals(200, resp.status_code)
        self.assertTrue(resp.json['success'])
        self.assertEquals(resp.json['data'], [dict(title='ham', slug='spam', item_count=10, current_count=2),
                                              dict(title='egg', slug='jam', item_count=5, current_count=3)])
