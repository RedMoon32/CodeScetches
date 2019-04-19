from datetime import datetime
from database.DBApi import DBEntity, ForeignKey, get_seconds_from_midnight
from database.DBApi import Connection


class User(DBEntity):
    def __init__(self,
                 username: str,
                 first_name: str = '',
                 last_name: str = '',
                 password: str = '',
                 age: int = 0,
                 sex: str = 'Male',
                 address: str = '',
                 history: str = '',
                 contact: str = ''):
        super().__init__(dbid=username)
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.age = age
        self.address = address
        self.sex = sex
        self.history = history
        self.contact = contact

    def save(self, con: Connection):
        # There is no doctors, patients.. etc
        # (users of different type) with the same id
        if User.get_type_by_id(self.id, con) is 'user':
            return super(User, self).save(con)
        else:
            return False

    @staticmethod
    def get_user_with_correct_type(dbid, con):
        user_type = User.get_type_by_id(dbid, con)
        if user_type is 'patient':
            return Patient.get_by_id(dbid, con)
        if user_type is 'employee':
            return Employee.get_by_id(dbid, con)
        if user_type is 'doctor':
            return Doctor.get_by_id(dbid, con)
        if user_type is 'nurse':
            return Nurse.get_by_id(dbid, con)
        if user_type is 'receptionist':
            return Receptionist.get_by_id(dbid, con)

        return User.get_by_id(dbid, con)

    @staticmethod
    def get_type_by_id(uid, con: Connection):
        if Employee.get_by_id(uid, con) is not None:
            return 'employee'
        if Doctor.get_by_id(uid, con) is not None:
            return 'doctor'
        if Patient.get_by_id(uid, con) is not None:
            return 'patient'
        if Nurse.get_by_id(uid, con) is not None:
            return 'nurse'
        if Receptionist.get_by_id(uid, con) is not None:
            return 'receptionist'
        return 'user'


class Patient(User):
    def __init__(self,
                 username: str,
                 first_name: str = '',
                 last_name: str = '',
                 password: str = '',
                 age: int = 0,
                 sex: str = 'Male',
                 address: str = '',
                 history: str = '',
                 contact: str = ''):
        super().__init__(username=username,
                         first_name=first_name,
                         last_name=last_name,
                         password=password,
                         age=age,
                         sex=sex,
                         address=address,
                         history=history,
                         contact=contact)

    def get_records(self, con):
        records = []
        for r in con.client.smembers('one_to_many:' + self.key + ':' + Appointment.__name__.lower()):
            record = Appointment.get_by_key(r, con)
            if record is not None:
                records.append(record)
        return records


class Employee(User):
    def __init__(self,
                 username: str,
                 first_name: str = '',
                 last_name: str = '',
                 password: str = '',
                 age: int = 0,
                 sex: str = 'Male',
                 address: str = '',
                 history: str = '',
                 contact: str = '',
                 salary: int = 0):
        super().__init__(username=username,
                         first_name=first_name,
                         last_name=last_name,
                         password=password,
                         age=age,
                         address=address,
                         sex=sex,
                         history=history,
                         contact=contact)
        self.salary = salary


class Receptionist(Employee):
    pass


class Nurse(Employee):
    pass


class Doctor(Employee):
    def get_appointments(self, con):
        records = []
        for r in con.client.smembers('one_to_many:' + self.key + ':' + Appointment.__name__.lower()):
            record = Appointment.get_by_key(r, con)
            if record is not None:
                records.append(record)
        return records


class Appointment(DBEntity):
    def __init__(self,
                 description: str = '',
                 patient: Patient = Patient('null'),
                 doctor: Doctor = Doctor('null'),
                 date: str = str(datetime.now().date()),
                 time: int = get_seconds_from_midnight(),
                 time_slot: int = 0
                 ):
        key = f"{date}-{str(time)}"
        super().__init__(key)
        self.description = description
        self.patient = ForeignKey(patient.key)
        self.doctor = ForeignKey(doctor.key)
        self.time_slot = time_slot
        self.date = date
        self.time = time

    def get_patient(self, con):
        # None if deleted
        return Appointment.get_by_key(self.patient.key, con)

    def get_doctor(self, con):
        # None if deleted
        return Receptionist.get_by_key(self.doctor.key, con)
