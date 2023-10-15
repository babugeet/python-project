import unittest
from unittest.mock import patch
import os
import phonebook
from phonebook import PhoneBook
import sqlite3
import sys

# from phonebook import create_table create_db
DBNAME="test_phonebook.db"
class Testphonebook(unittest.TestCase):
    # @classmethod
    # def setUp(self) -> None:
    #     phonebook.create_db(DBNAME)
        # return super().setUp()
    @classmethod
    def setUpClass(cls):
        phonebook.create_db(DBNAME)
        # print("reached setup class")
    
    def test_tes(self):
         pass
    def test_create_table(self):
        phonebook.create_table(DBNAME)
        conn = sqlite3.connect(DBNAME) 
        c = conn.cursor()
        stmt = "select * from phonebook"
        try:
            c.execute(stmt)
        except sqlite3.OperationalError:
             self.fail("sql Table not found")
        result = c.fetchone()
        conn.commit()
        c.close()
        # print(result)
        self.assertIsNone(result, msg=None)
class TestAddDB(unittest.TestCase):
    @patch('phonebook.DB_NAME',DBNAME)
    def setUp(self):
        self.test_dict= {
            "name": "John Doe",
            "age": 30,
            "place": "New York",
            "phone": 1234567890,
            "password": "hashed_password"
        }
        phonebook.create_table(DBNAME)
        conn = sqlite3.connect(DBNAME) 
        c = conn.cursor()
        conn.commit()
        c.close()
        self.phone_book=phonebook.PhoneBook(self.test_dict)

    @patch('phonebook.DB_NAME',DBNAME)
    def test_add_db_user(self):
        self.phone_book.add_db()
        #verify if user present
        c=phonebook.verify_user_on_db( self.test_dict["name"])
        self.assertIsNot(len(c.fetchall()) , 0)
    @patch('phonebook.DB_NAME',DBNAME)
    def test_add_db_userfailure(self):
        c=phonebook.verify_user_on_db( "name")
        self.assertIs(len(c.fetchall()) , 0)
    @patch('phonebook.DB_NAME',DBNAME)
    def test_delete_user(self):
        phonebook.delete_user("John Doe")
        c=phonebook.verify_user_on_db("John Doe")
        self.assertIs(len(c.fetchall()) , 0)


    @classmethod
    def tearDownClass(cls) -> None:
        os.remove("test_phonebook.db")
        return super().tearDownClass()

class TestOperatorSelection(unittest.TestCase):
    def setUp(self):
        self.original_arg=sys.argv

    def tearDown(self):
        sys.argv=self.original_arg
    @patch('sys.argv',["test_phonebook.py"])
    def test_nouserinput(self):
        with self.assertRaises(SystemExit) as cm:
              phonebook.operator_selection()
        self.assertEqual(cm.exception.code,1)
    @patch('sys.argv',["test_phonebook.py","add","delete"])
    def test_multipleuserinput(self):
        with self.assertRaises(SystemExit)as cm:
            phonebook.operator_selection()
        self.assertEqual(cm.exception.code,1)
    @patch('sys.argv',["test_phonebook.py","add"])
    def test_userinput_add(self):
        output=phonebook.operator_selection()
        self.assertEqual(output,"add")
    @patch('sys.argv',["test_phonebook.py","delete"])
    def test_userinput_delete(self):
        output=phonebook.operator_selection()
        self.assertEqual(output,"delete")
    @patch('sys.argv',["test_phonebook.py","read"])
    def test_userinput_read(self):
        output=phonebook.operator_selection()
        self.assertEqual(output,"read")

class TestPassword(unittest.TestCase):
    # def setUp(self):
    #     pass
    # def tearDown(self):
    #     pass
    @patch('phonebook.password_input', side_effect=['password123', 'password123'])
    def test_valid_password(self, mock_password_input):
        password = phonebook.take_password()
        self.assertEqual(password, 'password123')

    @patch('phonebook.password_input', side_effect=['password123', 'password23','password123', 'password23','password123', 'password23'])
    def test_wrong_password_rentry(self, mock_password_input):
        with self.assertRaises(SystemExit) as cm:
              password = phonebook.take_password()
        self.assertEqual(cm.exception.code,2)
    @patch('phonebook.password_input', side_effect=['password123', 'password23','password123', 'password23','password123', 'password123'])
    def test_right_password_last_try(self, mock_password_input):
        password = phonebook.take_password()
        self.assertEqual(password, 'password123')
if __name__=='__main__':
	unittest.main()