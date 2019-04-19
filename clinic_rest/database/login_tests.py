from datetime import datetime
import unittest

from database.models import Employee
from database.DBApi import db_connection
from database.login import *


class MyTestCase(unittest.TestCase):
    def test_login(self):

        con = db_connection
        con.client.flushall()
        emp = registration('lolkek', '123', 20, 'Male', 'pnx', con)
        usernew = login('lolkek', '123', con)
        emp_fetched = User.get_by_id('lolkek', con)

        print(emp.__dict__)
        print(usernew.__dict__)
        print(emp_fetched.__dict__)

        self.assertTrue(emp.__dict__ == usernew.__dict__ == emp_fetched.__dict__)
        self.assertEqual(usernew.key, emp.key)
        self.assertEqual(usernew.type, emp.type)


if __name__ == '__main__':
    unittest.main()
