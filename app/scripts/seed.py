import requests
import json

POST_END_POINT = "https://jsonplaceholder.typicode.com/posts"
USER_END_POINT = "https://jsonplaceholder.typicode.com/users"

def fake_users(method='GET', data={}, is_json=True):
    if not is_json:
        data = json.dumps(data)
    res = requests.request(method, USER_END_POINT, data=data)

    objects = res.json()

    for obj in objects:
      response ={
        'email':obj['email'],
        'name':obj['name'],
        'password':obj['email'].lower(),
      }
      res = requests.post('http://127.0.0.1:8000/api/user/create/', response)
      print(res.status_code)
    return res


def fake_post(method='GET', data={}, is_json=True):
    if not is_json:
        data = json.dumps(data)
    res = requests.request(method, POST_END_POINT, data=data)

    objects = res.json()

    for obj in objects:
      response ={
        'user_id': 2,
        'title':obj['title'],
        'body':obj['body'],
        'tags':'1',
      }
      res = requests.post('http://127.0.0.1:8000/api/post/', response)
      print(res.status_code)
    return res
      

fake_post()
fake_users()

