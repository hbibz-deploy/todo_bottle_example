from api import app
from webtest import TestApp, AppError
import json
import redis

wsgi = TestApp(app.bottle_app)

auth_token = None

def setup():
  app._redis = redis.StrictRedis(port=6389)

def test_wsgi_post_login_success():
  resp = wsgi.post('/api/login', dict(username='test_user', password='password'))
  assert resp.status_code == 200
  assert resp.json['auth_token']
  global auth_token
  auth_token = resp.json['auth_token']

def test_wsgi_post_todo_success():
  post_data = dict(
    title='a test todo title',
    dueDate=1362355210010,
    labels=[
      'test_label1', 
      'test_label2'
    ],
    completed=False,
    auth_token=auth_token
  )
  resp = wsgi.post_json('/api/todos', post_data)
  assert resp.status_code == 200

def test_wsgi_put_todo_success():
  dueDate = 1362355210010
  post_data = dict(
    title='a test todo title',
    dueDate=dueDate,
    labels=[
      'test_label1', 
      'test_label2'
    ],
    completed=False
  )
  resp = wsgi.post_json('/api/todos', post_data)
  new_id = str(resp.json['id'])
  post_data['id'] = new_id
  post_data['dueDate'] = dueDate + 10
  resp = wsgi.put_json('/api/todos/'+new_id, post_data)
  assert resp.status_code == 200
  assert int(resp.json['dueDate']) == dueDate + 10

def test_wsgi_get_todos_success():
  resp = wsgi.get('/api/todos')
  assert resp.status_code == 200

def test_wsgi_get_todos_with_sort_by_title_success():
  resp = wsgi.get('/api/todos?sortBy=title')
  assert resp.status_code == 200

def test_wsgi_get_todos_with_tag_filter_success():
  resp = wsgi.get('/api/todos?tagFilter=test_label2')
  assert resp.status_code == 200

def test_wsgi_delete_todo_success():
  dueDate = 1362355210010
  post_data = dict(
    title='a test todo title',
    dueDate=dueDate,
    labels=[
      'test_label1', 
      'test_label2'
    ],
    completed=False
  )
  resp = wsgi.post_json('/api/todos', post_data)
  new_id = str(resp.json['id'])
  resp = wsgi.delete('/api/todos/'+new_id)
  assert resp.status_code == 200
  assert int(resp.json['success']) == True

def test_wsgi_get_labels_success():
  resp = wsgi.get('/api/labels')
  assert resp.status_code == 200


