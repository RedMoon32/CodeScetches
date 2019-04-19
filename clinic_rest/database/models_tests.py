import unittest
from database.models import *
from database.DBApi import Connection


class DBTests(unittest.TestCase):

    def test_indexing(self):

        con = Connection(port=6379)
        con.client.flushall()

        p = Patient(username="sashokPetushok")
        r = Receptionist(username='sashokLoshok')
        d = Doctor(username='DoctorWho')
        p.save(con)
        r.save(con)
        d.save(con)

        # Create Records and push them in Redis. all linked to, 'p', 'd'
        appointments_list = []
        for i in range(10):
            created_entity = Appointment(str(i), description='desc #' + str(i), patient=p, doctor=d)
            if created_entity.save(con):
                appointments_list.append(created_entity.key)

        print(con.client.keys('*'))

        # Get list of pushed Records from Redis
        db_list = []
        for rec in d.get_appointments(con):
            db_list.append(rec.key)

        # Print lists to see why we need to sort them in compare
        print(appointments_list)
        print(db_list)

        # Test whether initial entities' key and fetched entities' key are the same)
        self.assertTrue(compare(appointments_list, db_list))

        print('all appointments: ', Appointment.get_all(con))

        app = Appointment.get_by_id('df1', con)
        if app is not None:
            doc = app.get_doctor(con)
            print(d.key == doc.key)
            self.assertTrue(d.key == doc.key)

        # Delete all created entities from redis and (if current removal is successful) delete from initial list
        for i in range(10):
            entity_to_delete = Appointment.get_by_id(str(i), con)
            if entity_to_delete.delete(con):
                appointments_list.remove(entity_to_delete.key)

        # fetch all RELATED to receptionist Records (there must be no records because we deleted them)
        db_list = []
        for rec in d.get_appointments(con):
            db_list.append(rec.key)

        # check whether there are no records in initial list and in fetched (via receptionist) records
        self.assertTrue([] == appointments_list == db_list)

        p.delete(con)
        r.delete(con)
        d.delete(con)
        print(con.client.keys('*'))

    def test_type_checking(self):

        con = Connection(port=6379)
        con.client.flushall()

        e = Employee('employee@example.com')
        d = Doctor('doctor@example.com')
        n = Nurse('nurse@example.com')
        u = User('user@example.com')
        p = Patient('patient@example.com')

        e.save(con)
        d.save(con)
        n.save(con)
        u.save(con)
        p.save(con)

        print(User.get_type_by_id(e.id, con=con))
        print(User.get_type_by_id(d.id, con=con))
        print(User.get_type_by_id(n.id, con=con))
        print(User.get_type_by_id(u.id, con=con))
        print(User.get_type_by_id(p.id, con=con))

        self.assertTrue(User.get_type_by_id(e.id, con=con) is 'employee')
        self.assertTrue(User.get_type_by_id(d.id, con=con) is 'doctor')
        self.assertTrue(User.get_type_by_id(n.id, con=con) is 'nurse')
        self.assertTrue(User.get_type_by_id(u.id, con=con) is 'user')
        self.assertTrue(User.get_type_by_id(p.id, con=con) is 'patient')

    # Check that we can not save
    # 'patient:same@sameemail.com' and
    # 'doctor:same@sameemail.com'
    def test_users_id_uniqueness(self):
        con = Connection(port=6379)

        p = Patient('lolkek')
        e = Employee('lolkek')
        p.save(con)
        result = e.save(con)

        self.assertTrue(result is False)

        pf = Patient.get_by_id('lolkek', con)
        ef = Employee.get_by_id('lolkek', con)

        self.assertTrue(pf.id == 'lolkek')
        self.assertTrue(ef is None)

    def test_appointments(self):
        con = Connection(port=6379)
        con.client.flushall()

        doc = Doctor('doctor@mail.rf')
        doc.save(con)
        pat = Patient('patient@mail.ru')
        pat.save(con)

        app = Appointment('appointment', 'blabla', pat, doc)
        app.save(con)

        app_fetched = Appointment.get_by_id('appointment', con)

        print(app.__dict__)
        print(app_fetched.__dict__)

        d1 = app.__dict__.copy()
        del d1['doctor']
        del d1['patient']

        d2 = app.__dict__.copy()
        del d2['doctor']
        del d2['patient']

        self.assertTrue(d1 == d2)

    def test_appointments_date(self):
        con = Connection(port=6379)
        con.client.flushall()

        doc = Doctor('doctor@mail.rf')
        doc.save(con)
        pat = Patient('patient@mail.ru')
        pat.save(con)

        app = Appointment('appointment', 'blabla', pat, doc, time=75000, date='2019-04-12', time_slot=3)
        app.save(con)

        app_fetched = Appointment.get_by_id('appointment', con)

        print(Appointment('appointment', 'blabla', pat, doc, time_slot=3).__dict__)

        self.assertTrue(app_fetched.doctor.key == app.doctor.key)
        self.assertTrue(app_fetched.doctor.id == app.doctor.id)
        self.assertTrue(app_fetched.time == app.time)


def compare(s, t):
    return sorted(s) == sorted(t)


if __name__ == '__main__':
    unittest.main()
