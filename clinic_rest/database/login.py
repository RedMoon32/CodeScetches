from database.models import User, Employee
from database.DBApi import Connection

connection = Connection

from database.models import Employee, Receptionist, Patient, Appointment
from database.DBApi import Connection

# connection = Connection

connection = Connection


def login(email: str, password: str, con):
    user = User.get_user_with_correct_type(email, con)
    if user is not None and user.password == password:
        return user
    else:
        return None


def registration(username: str,
                 password: str,
                 age: int,
                 sex: str,
                 address: str,
                 first_name: str,
                 last_name: str,
                 con: Connection):
    user = Employee(username=username,
                    password=password,
                    age=age,
                    sex=sex,
                    address=address,
                    first_name=first_name,
                    last_name=last_name,
                    )

    if user.save(con):
        return user
    else:
        return None  # User already exist
