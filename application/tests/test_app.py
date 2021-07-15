from flask import url_for
from flask_testing import TestCase

from application import app, db
from application.models import Task

class TestBase(TestCase):
    def create_app(self):

        app.config.update(SQLALCHEMY_DATABASE_URI="sqlite:///",
                SECRET_KEY='TEST_SECRET_KEY',
                DEBUG=True,
                WTF_CSRF_ENABLED=False)

        return app

    def setUp(self):
        db.create_all()

        sample=Task(name='Potato',description='Wash the potato',complete=False)

        db.session.add(sample)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestViews(TestBase):
    def test_read_get(self):
        response=self.client.get(url_for('read'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Potato',response.data)

class TestAdd(TestBase):
    def test_add(self):
        response=self.client.post(url_for('add'), data = dict(name='Avocado',description='Eat the avocado'),follow_redirects=True)
        self.assertIn(b'Added the new task!',response.data)
        response=self.client.get(url_for('read'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Avocado',response.data)

class TestUpdate(TestBase):
    def test_update(self):
        response=self.client.post(url_for('update'), data = dict(name='Potato',description='Eat the potato'),follow_redirects=True)
        self.assertIn(b'Updated the task!',response.data)
        response=self.client.get(url_for('read'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Eat the potato',response.data)

class TestDelete(TestBase):
    def test_delete(self):
        response=self.client.post(url_for('delete'), data = dict(name='Potato'),follow_redirects=True)
        self.assertIn(b'Deleted the task!',response.data)
        response=self.client.get(url_for('read'))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Potato',response.data)