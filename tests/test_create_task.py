from flask import url_for
from . import BaseTest, dbsession as s
from raiden.models import Task


class CreateTaskTest(BaseTest):
    def test_endpoint_exists(self):
        resp = self.client.post(url_for('create_task'), data={'title': 'Spam', 'item_count': 73})
        self.assertNotEquals(404, resp.status_code)

    def test_returns_task_slug_and_success_flag_and_empty_message(self):
        resp = self.client.post(url_for('create_task'), data={'title': 'Spam', 'item_count': 73})
        self.assertRegexpMatches(resp.json['slug'], '^[0-9a-f]{32}$')
        self.assertIsInstance(resp.json['success'], bool)
        self.assertEquals(resp.json['msg'], '')

    def test_create_persist_task(self):
        resp = self.client.post(url_for('create_task'), data={'title': 'Spam', 'item_count': 73})
        result = s.query(Task.title, Task.item_count).all()

        self.assertEquals([('Spam', 73)], result)

    def test_returns_task_random_slug(self):
        slug_1 = self.client.post(url_for('create_task'), data={'title': 'Spam', 'item_count': 73}).json['slug']
        slug_2 = self.client.post(url_for('create_task'), data={'title': 'Spam', 'item_count': 73}).json['slug']
        slug_3 = self.client.post(url_for('create_task'), data={'title': 'Ops', 'item_count': 21}).json['slug']

        self.assertNotEquals(slug_1, slug_2)
        self.assertNotEquals(slug_2, slug_3)
        self.assertNotEquals(slug_1, slug_3)

        self.assertItemsEqual(s.query(Task.slug).all(), [(slug_1,), (slug_2,),(slug_3,)])

    def test_returns_400_error_in_invalid_input_with_correspondent_message(self):
        # missing 'title'
        resp_1 = self.client.post(url_for('create_task'), data={'item_count': 4})
        self.assertEquals(resp_1.status_code, 400)
        self.assertFalse(resp_1.json['success'], 'Request should not be successful')
        self.assertEquals(resp_1.json['msg'], "'title' field is mandatory")

        # missing 'item_count'
        resp_2 = self.client.post(url_for('create_task'), data={'title': 'Ops'})
        self.assertEquals(resp_2.status_code, 400)
        self.assertFalse(resp_2.json['success'], 'Request should not be successful')
        self.assertEquals(resp_2.json['msg'], "'item_count' field is mandatory")

        # 'item_count' should be integer
        resp_3 = self.client.post(url_for('create_task'), data={'title': 'Spam', 'item_count': 'Ham'})
        self.assertEquals(resp_3.status_code, 400)
        self.assertFalse(resp_3.json['success'], 'Request should not be successful')
        self.assertEquals(resp_3.json['msg'], "'item_count' should be an integer")
