from django.test import TestCase
from rest_framework.test import APIClient
from database.DBApi import db_connection
import json
from database.models import *
from database.login import *

# numbers
pn = dn = un = 0


def get_random_patient(get_dict=False):
    global pn
    test_user = {'first_name': 'a', 'last_name': 'b',
                 'age': 35, 'password': '444',
                 'sex': 'male', 'address': 'Moscow', 'contact': '4444', 'username': f'a{str(pn)}'}
    patient = Patient(**test_user)
    pn += 1
    if get_dict:
        return patient, test_user
    else:
        return patient


def get_random_user(get_dict=False):
    global un
    test_user = {'username': f'test{str(un)}@mail.ru', 'password': '123', 'age': 30,
                 'sex': 'male', 'address': 'Moscow', 'first_name': 'a', 'last_name': 'b', }
    user = User(username=test_user['username'], password=test_user['password'])
    un += 1
    if get_dict:
        return user, test_user
    else:
        return user


def get_random_doctor(get_dict=False):
    global dn
    test_user = {'username': f'doc{str(dn)}x@mail.ru', 'password': str(hash("123")), 'age': 35,
                 'sex': 'male', 'address': 'Moscow', 'first_name': 'a', 'last_name': 'b', }
    d1 = Doctor(**test_user)
    dn += 1
    if get_dict:
        return d1, test_user
    else:
        return d1


class ClinicTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        db_connection.client.flushall()

    def testLogin(self):
        # Test login api with correct/incorrect data

        user, test_user = get_random_user(True)

        user.delete(db_connection)

        resp = self.client.post('/login/', data=test_user, format='json')
        self.assertTrue(resp.status_code == 401)
        registration(**test_user,
                     con=db_connection)
        resp = self.client.post('/login/')
        self.assertTrue(resp.status_code == 401)

        resp = self.client.post('/login/',
                                test_user,
                                format='json')
        self.assertTrue(resp.status_code == 200)
        user.delete(db_connection)

    def testReg(self):
        # Test registration api & check that can not register two times
        user, test_user = get_random_user(True)

        resp = self.client.post('/register/', data=test_user, format='json')
        self.assertTrue(resp.status_code == 200)
        resp = self.client.post('/register/', data=test_user, format='json')
        self.assertTrue(resp.status_code == 400)
        user.delete(db_connection)

    def testRegLogProfile(self):
        # Test that registered user  can log in to the system(get token) and by this token
        # can get his profile
        user, test_user = get_random_user(True)
        user.delete(db_connection)

        resp = self.client.post('/register/', data=test_user, format='json')
        self.assertTrue(resp.status_code == 200)
        resp = self.client.post('/login/', data=test_user, format='json')
        self.assertTrue(resp.status_code == 200)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + resp.data['token'])
        resp = self.client.get('/profile/')
        self.assertTrue(resp.status_code == 200)
        test_user.pop('password')
        self.assertEqual(resp.data , test_user)
        user.delete(db_connection)

    def testNotLoggedProfile(self):
        # Test that not logged user(or user with wrong token) can not get profile
        user, test_user = get_random_user(True)
        registration(**test_user,
                     con=db_connection)
        resp = self.client.get('/profile/')
        self.assertTrue(resp.status_code == 401)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(hash(123)))
        resp = self.client.get('/profile/')
        self.assertTrue(resp.status_code == 401)

    def loginDoc(self):
        # Log in as Doctor

        d1, test_user = get_random_doctor(True)
        d1.save(db_connection)
        resp = self.client.post('/login/', data=test_user, format='json')
        self.assertTrue(resp.status_code == 200)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + resp.data['token'])
        return d1

    def testAppointmentDoctorCreation(self):
        # test that doctor can assign new appointments to himself
        logged_doctor = self.loginDoc()
        p1, test_user = get_random_patient(True)
        p1.save(db_connection)

        resp = self.client.post('/appointments/',
                                data=json.dumps(
                                    {'doctor': logged_doctor.id, 'patient': p1.id, 'date': '11.20.2009', 'time': '5'}),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        apps = p1.get_records(db_connection)
        self.assertTrue(len(apps) == 1)
        self.assertTrue(apps[0].doctor.key == logged_doctor.key)
        self.assertTrue(apps[0].patient.key == p1.key)

    def testAppointmentPatientCreation(self):
        # Test that Patient can create appointments
        p1, logged_patient = get_random_patient(get_dict=True)
        p1.save(db_connection)
        resp = self.client.post('/login/', data=logged_patient, format='json')
        self.assertTrue(resp.status_code == 200)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + resp.data['token'])
        d1 = get_random_doctor()
        d1.save(db_connection)
        resp = self.client.post('/appointments/',
                                data=
                                {'doctor': d1.id, 'patient': p1.id, 'date': '11.20.2019', 'time': 5},
                                format='json')
        self.assertEqual(resp.status_code, 200)
        apps = d1.get_appointments(db_connection)
        self.assertTrue(len(apps) == 1)
        self.assertTrue(apps[0].doctor.key == d1.key)
        self.assertTrue(apps[0].patient.key == p1.key)

        p1, logged_patient = get_random_patient(get_dict=True)
        p1.save(db_connection)
        resp = self.client.post('/appointments/',
                                data=
                                {'doctor': d1.id, 'patient': p1.id, 'date': '11.20.2019', 'time': 5},
                                format='json')
        self.assertEqual(resp.status_code, 400)

    def loginAsPatient(self):
        # create a user log in as patient
        p1, test_user = get_random_patient(get_dict=True)
        p1.save(db_connection)
        resp = self.client.post('/login/', data=test_user, format='json')
        self.assertTrue(resp.status_code == 200)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + resp.data['token'])
        return p1

    def testAppointent(self):
        # test that user can create appointment but only if (doctor, timeslot) is available
        p1 = self.loginAsPatient()

        d1 = get_random_doctor()
        d1.save(db_connection)
        resp = self.client.post('/appointments/',
                                data=
                                {'doctor': d1.id, 'patient': p1.id, 'date': '11.20.2019', 'time': 5},
                                format='json')
        self.assertEqual(resp.status_code, 200)
        p1 = self.loginAsPatient()
        resp = self.client.post('/appointments/',
                                data=
                                {'doctor': d1.id, 'patient': p1.id, 'date': '11.20.2019', 'time': 5},
                                format='json')
        self.assertEqual(resp.status_code, 400)

    def testGetAppointments(self):
        # test that user creates one appointment and gets it
        p1 = self.loginAsPatient()
        d1 = get_random_doctor()
        d1.save(db_connection)
        resp = self.client.post('/appointments/',
                                data=
                                {'doctor': d1.id, 'patient': p1.id, 'date': '11.20.2119', 'time': 5},
                                format='json')
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get('/appointments/')
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data, [{'doctor': d1.id, 'patient': p1.id, 'date': '11.20.2119', 'time': 5}])
        self.assertTrue(True)

        p1 = self.loginAsPatient()
        resp = self.client.get('/appointments/')
        self.assertEqual(len(resp.data), 0)

    def test_get_all_doctors(self):
        d = [get_random_doctor().save(db_connection) for i in range(5)]
        resp = self.client.get('/doctors/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 5)
