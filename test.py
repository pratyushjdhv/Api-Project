import unittest
import json
from api import app, db, todo_list, todo_task

class TodoApiTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_todo_item(self):
        payload = {
            "title": "Daily Tasks",
            "task": "Complete unit testing"
        }
        response = self.app.post('/todo', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Todo-list created', response.data)

    def test_get_all_todo_items(self):
        payload = {
            "title": "Daily Tasks",
            "task": "Complete unit testing"
        }
        self.app.post('/todo', data=json.dumps(payload), content_type='application/json')

        response = self.app.get('/todo/task')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("Daily Tasks", [todo['title'] for todo in data['tasks']])

    def test_get_single_todo_item(self):
        payload = {
            "title": "Daily Tasks",
            "task": "Complete unit testing"
        }
        self.app.post('/todo', data=json.dumps(payload), content_type='application/json')

        with app.app_context():
            todo = todo_list.query.filter_by(title="Daily Tasks").first()
            response = self.app.get(f'/todo/task/{todo.id}')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIn("Complete unit testing", data['tasks'])

    def test_update_todo_item(self):
        payload = {
            "title": "Daily Tasks",
            "task": "Complete unit testing"
        }
        self.app.post('/todo', data=json.dumps(payload), content_type='application/json')

        with app.app_context():
            todo_task_item = todo_task.query.filter_by(task="Complete unit testing").first()
            update_payload = {
                "task": "Complete unit testing and review code"
            }
            response = self.app.put(f'/todo/{todo_task_item.id}', data=json.dumps(update_payload), content_type='application/json')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Task updated', response.data)

    def test_delete_todo_item(self):
        payload = {
            "title": "Daily Tasks",
            "task": "Complete unit testing"
        }
        self.app.post('/todo', data=json.dumps(payload), content_type='application/json')

        with app.app_context():
            todo_task_item = todo_task.query.filter_by(task="Complete unit testing").first()
            response = self.app.delete(f'/todo/{todo_task_item.id}')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Task deleted', response.data)

if __name__ == '__main__':
    unittest.main()
