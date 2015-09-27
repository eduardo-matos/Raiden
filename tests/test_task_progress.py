from mock import patch, call
from flask import url_for
from . import BaseTest, dbsession as s
from raiden.models import Task


class ProgressTaskTest(BaseTest):
    def setUp(self):
        self.task = Task(title='Ham', item_count=10, slug='d41d8cd98f00b204e9800998ecf8427e')
        s.add(self.task)
        s.commit()

    def test_updates_task_progress(self):
        self.assertEquals(self.task.current_count, 0)

        resp = self.client.post(url_for('progress_task', slug=self.task.slug), data={'current_count': 4})

        task = s.query(Task).first()
        self.assertEquals(self.task.current_count, 4)

    def test_returns_task_current_count(self):
        resp = self.client.post(url_for('progress_task', slug=self.task.slug), data={'current_count': 6})
        self.assertEquals(resp.json['current_count'], 6)
        self.assertEquals(resp.json['success'], True)

    def test_emit_websocket_signal(self):
        with patch('raiden.views.socketio') as socketio:
            resp = self.client.post(url_for('progress_task', slug=self.task.slug), data={'current_count': 6})

            self.assertEquals([call('progress_task', {'current_count': 6, 'slug': self.task.slug})],
                              socketio.emit.call_args_list)
    def test_updates_specific_task(self):
        s.add(Task(title='Ham', item_count=10, slug='e09f6a7593f8ae3994ea57e1117f67ec'))
        s.commit()

        resp = self.client.post(url_for('progress_task', slug='e09f6a7593f8ae3994ea57e1117f67ec'),
                                data={'current_count': 6})

        task_1 = s.query(Task.current_count).filter(Task.id == self.task.id).first()
        task_2 = s.query(Task.current_count).filter(Task.slug == 'e09f6a7593f8ae3994ea57e1117f67ec').first()
        self.assertEquals(task_1.current_count, 0)
        self.assertEquals(task_2.current_count, 6)

    def test_returns_400_error_in_invalid_input_with_correspondent_message(self):
        # 'current_count' should be integer
        resp = self.client.post(url_for('progress_task', slug=self.task.slug), data={'current_count': 'spam'})
        self.assertEquals(resp.status_code, 400)
        self.assertFalse(resp.json['success'], 'Request should not be successful')
        self.assertEquals(resp.json['msg'], "'current_count' should be an integer")
