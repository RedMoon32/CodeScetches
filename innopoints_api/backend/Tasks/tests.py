from django.test import TestCase
from Tasks.models import *
from profile.models import UserProfile
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

import json

acp = "ACCEPTED"
dcl = "DECLINED"

task = {'title': 't1', 'description': 'd1', 'inno_points': 10, 'event_time': '2099-11-30'}


class TaskTest(TestCase):
    api_client = APIClient()

    @classmethod
    def setUpTestData(cls):
        for i in range(1, 6):
            user = User.objects.create_user(username='u{}'.format(i), email='test@mail.com')
            UserProfile.objects.create(user_id=i)
            Token.objects.create(user=user)

    def setUp(self):
        self.relogin(username='u1')

    def relogin(self, username=None, user=None):
        if not user:
            self.logged_user = User.objects.get(username=username)
            self.api_client.force_authenticate(self.logged_user)
        else:
            self.api_client.force_authenticate(user)

    def test_create(self):
        response = self.api_client.post('/tasks/',
                                        data=task)
        task2 = dict(task)
        task2['applications'] = []
        self.assertTrue(response.data, task2)

    def test_get(self):
        for i in range(3):
            Task.objects.create(**task, owner=UserProfile.objects.get(user__username='u1'))
        self.relogin('u2')
        response = self.api_client.get('/tasks/')
        self.assertTrue(len(response.data) == 3)

    def test_apply(self):
        id = Task.objects.create(**task).id
        id = \
            self.api_client.post('/applications/my/', data=json.dumps({'id': id}),
                                 content_type='application/json').data[
                'id']
        self.assertTrue(Application.objects.get(id=id) ==
                        Application(id=id, volunteer=UserProfile.objects.get(user=self.logged_user), task_id=1))

    def test_get_applications(self):

        owner = User.objects.get(username='u1')
        id = Task.objects.create(**task, owner=UserProfile.objects.get(user=owner)).id
        for i in range(2, 5):
            self.relogin(username='u{}'.format(i))

            self.api_client.post('/applications/my/', data=json.dumps({'id': id}), content_type='application/json')

        self.relogin(user=owner)

        response = self.api_client.get('/applications/', {'id': id})
        self.assertTrue(len(response.data) == 3)

    def test_get_user_applications(self):
        owner = User.objects.get(username='u1')
        self.relogin(username='u2')
        for i in range(10):
            id = Task.objects.create(**task, owner=UserProfile.objects.get(user=owner)).id
            self.api_client.post('/applications/my/', data=json.dumps({'id': id}), content_type='application/json')
        response = self.api_client.get('/applications/my/')
        self.assertTrue(len(response.data) == 10)

    def test_update_application_status(self):
        owner = User.objects.get(username='u1')
        id = Task.objects.create(**task, owner=UserProfile.objects.get(user=owner)).id
        ids = []
        for i in range(2, 5):
            self.relogin(username='u{}'.format(i))
            ids.append(self.api_client.post('/applications/my/', data=json.dumps({'id': id}),
                                            content_type='application/json').data['id'])
        self.assertTrue(Application.objects.count() == 3)
        self.relogin(user=owner)
        self.api_client.post('/applications/', data=json.dumps({'id': ids[0], 'status': acp}),
                             content_type='application/json')
        self.api_client.post('/applications/', data=json.dumps({'id': ids[1], 'status': dcl}),
                             content_type='application/json')
        self.api_client.post('/applications/', data=json.dumps({'id': ids[2], 'status': acp}),
                             content_type='application/json')

        self.assertTrue(Application.objects.get(id=ids[0]).status == acp)
        self.assertTrue(Application.objects.get(id=ids[1]).status == dcl)
        self.assertTrue(Application.objects.get(id=ids[2]).status == acp)

    def test_close_application(self):
        id = Task.objects.create(**task).id
        self.relogin(username='u2')
        id = \
            self.api_client.post('/applications/my/', data=json.dumps({'id': id}),
                                 content_type='application/json').data[
                'id']
        self.api_client.delete('/applications/my/', data=json.dumps({'id': id}), content_type='application/json')

        self.assertTrue(Application.objects.get(id=id).status == 'CANCELLED')

    def test_close_task(self):
        owner = User.objects.get(username='u1')
        task_id = Task.objects.create(**task, owner=UserProfile.objects.get(user=owner)).id
        ids = []
        for i in range(2, 5):
            self.relogin(username='u{}'.format(i))

            ids.append(self.api_client.post('/applications/my/', data=json.dumps({'id': task_id}),
                                            content_type='application/json').data['id'])

        self.relogin(user=owner)
        self.api_client.post('/applications/', data=json.dumps({'id': ids[0], 'status': acp}),
                             content_type='application/json')
        self.api_client.post('/applications/', data=json.dumps({'id': ids[1], 'status': dcl}),
                             content_type='application/json')
        self.api_client.post('/applications/', data=json.dumps({'id': ids[2], 'status': acp}),
                             content_type='application/json')

        self.api_client.delete('/tasks/my/', data=json.dumps({'id': task_id}), content_type='application/json')
        apps = [Application.objects.get(id=i) for i in ids]
        self.assertTrue(
            apps[0].status == apps[2].status == 'FINISHED' and apps[1].status == 'DECLINED' and apps[0].inno_points ==
            apps[2].inno_points and apps[0].xp_points == apps[2].xp_points)

    def test_task_update(self):
        resp = self.api_client.post('/tasks/', data=json.dumps(task), content_type='application/json').data
        id_ = resp['id']
        resp['title'] = 't2'
        self.api_client.patch('/tasks/my/', data=json.dumps(resp), content_type='application/json')
        self.assertTrue(Task.objects.get(id=id_).title == 't2')

    def test_user_applications(self):
        new_task = Task.objects.create(**task, owner=UserProfile.objects.get(user=self.logged_user))
        task_id = new_task.id
        ids = []
        for i in range(2, 5):
            self.relogin(username='u{}'.format(i))
            ids.append(self.api_client.post('/applications/my/', data=json.dumps({'id': task_id}),
                                            content_type='application/json').data['id'])
        for i in range(2, 5):
            self.relogin(username='u{}'.format(i))
            resp = self.api_client.get('/applications/my/').data
            self.assertTrue(len(resp) == 1 and ids[i - 2] == resp[0]['id'])
        self.relogin('u1')
        self.assertTrue(len(self.api_client.get('/applications/', data={'id': task_id}).data) == 3)

    """ test that user can not apply after the deadline """

    def test_can_not_apply(self):
        new_task = dict(task)
        new_task['event_time'] = '2000-01-01'
        new_task = Task.objects.create(**new_task, owner=UserProfile.objects.get(user=self.logged_user))
        resp = self.api_client.post('/applications/my/', data=json.dumps({'id': new_task.id}),
                                    content_type='application/json')
        self.assertTrue(resp.status_code == 400)

    def test_partial_distribution(self):
        owner = User.objects.get(username='u1')
        id = Task.objects.create(**task, owner=UserProfile.objects.get(user=owner)).id
        ids = []
        for i in range(2, 6):
            self.relogin(username='u{}'.format(i))
            ids.append(self.api_client.post('/applications/my/', data=json.dumps({'id': id}),
                                            content_type='application/json').data['id'])
        self.assertTrue(Application.objects.count() == 4)
        self.relogin(user=owner)
        self.api_client.post('/applications/',
                             data=json.dumps({'id': ids[0], 'status': Application.FNS, 'inno_points': 10}),
                             content_type='application/json')
        self.api_client.post('/applications/', data=json.dumps({'id': ids[1], 'status': dcl}),
                             content_type='application/json')
        self.api_client.post('/applications/', data=json.dumps({'id': ids[2], 'status': acp}),
                             content_type='application/json')
        self.api_client.post('/applications/',
                             data=json.dumps({'id': ids[2], 'status': Application.FNS, 'inno_points': 10}),
                             content_type='application/json')

        self.api_client.post('/applications/', data=json.dumps({'id': ids[3], 'status': acp}),
                             content_type='application/json')
        self.api_client.post('/applications/',
                             data=json.dumps({'id': ids[3], 'status': Application.FNS, 'inno_points': 10000}),
                             content_type='application/json')

        app1 = Application.objects.get(id=ids[0])
        app2 = Application.objects.get(id=ids[1])
        app3 = Application.objects.get(id=ids[2])
        app4 = Application.objects.get(id=ids[3])

        # can not change PND to FNS
        self.assertTrue(app1.status != Application.FNS)
        self.assertTrue(app1.inno_points == 0)

        self.assertTrue(app2.status == dcl)
        self.assertTrue(app2.inno_points == 0)

        # can change ACP to FNS
        self.assertTrue(app3.status == Application.FNS)
        self.assertTrue(app3.inno_points == 10)

        # inno_points can not exceed task.inno_points attribute
        self.assertTrue(app4.status == Application.ACP)
        self.assertTrue(app4.inno_points == 0)
