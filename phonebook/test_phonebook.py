import unittest
from unittest.mock import patch,Mock
import os
import phonebook
from phonebook import PhoneBook
import sqlite3
import sys
import  passlib.hash
# from passlib.hash import bcrypt

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
        # self.assertIsNone(result, msg=None)
    @classmethod
    def tearDownClass(cls) -> None:
        os.remove(DBNAME)
        return super().tearDownClass()
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

class TestReadDB(unittest.TestCase):
    @patch('phonebook.DB_NAME',DBNAME)
    def setUp(self):
        self.test_dict= {
            "name": "John Doe",
            "age": 30,
            "place": "New York",
            "phone": 1234567890,
            "password": "$6$1RLMXI2.UJavKP7s$NAjikVAkF9qTxygdzSKWu3.XjHqYGPXBH0ut2CaYUTtxCdgRA8CBCdprYWtZcrKrFGScUB4iGMaTPF3W3ofDV1"
        }
        phonebook.create_table(DBNAME)
        conn = sqlite3.connect(DBNAME) 
        c = conn.cursor()
        conn.commit()
        c.close()
        self.phone_book=phonebook.PhoneBook(self.test_dict)
        self.phone_book.add_db()


    @patch("phonebook.verify_user_on_db")
    @patch("phonebook.take_password")
    @patch('passlib.hash.bcrypt.using')
    def test_user_found_correct_password(self,mock_bcrypt_using,mock_password,mock_verify_user_on_db):
        #arrangement
        mock_verify_user_on_db.return_value.fetchall.return_value=[(1)]
        mock_password.return_value="Abhi"
        mock_bcrypt_using.return_value.verify.return_value = True
        mock_verify_user_on_db.return_value.execute.return_value.fetchone.return_value= "$6$1RLMXI2.UJavKP7s$NAjikVAkF9qTxygdzSKWu3.XjHqYGPXBH0ut2CaYUTtxCdgRA8CBCdprYWtZcrKrFGScUB4iGMaTPF3W3ofDV1"
        # phonebook.hashed_password.fetchone.return_value = ("$6$1RLMXI2.UJavKP7s$NAjikVAkF9qTxygdzSKWu3.XjHqYGPXBH0ut2CaYUTtxCdgRA8CBCdprYWtZcrKrFGScUB4iGMaTPF3W3ofDV1",)
        phonebook.read_db('John Doe')

    @patch("phonebook.verify_user_on_db")
    @patch("phonebook.take_password")
    @patch('passlib.hash.bcrypt.using')
    def test_user_found_coerrect_password(self,mock_bcrypt_using,mock_password,mock_verify_user_on_db):
        #arrangement
        mock_verify_user_on_db.return_value.fetchall.return_value=[(1)]
        mock_password.return_value="Abhi"
        mock_bcrypt_using.return_value.verify.return_value = True
        mock_verify_user_on_db.return_value.execute.return_value.fetchone.return_value= "$6$1RLMXI2.UJavKP7s$NAjikVAkF9qTxygdzSKWu3.XjHqYGPXBH0ut2CaYUTtxCdgRA8CBCdprYWtZcrKrFGScUB4iGMaTPF3W3ofDV1"
        # phonebook.hashed_password.fetchone.return_value = ("$6$1RLMXI2.UJavKP7s$NAjikVAkF9qTxygdzSKWu3.XjHqYGPXBH0ut2CaYUTtxCdgRA8CBCdprYWtZcrKrFGScUB4iGMaTPF3W3ofDV1",)
        phonebook.read_db('John Doe')

    @patch('phonebook.verify_user_on_db')
    @patch('phonebook.take_password')
    @patch('passlib.hash.bcrypt.using')
    def test_user_found_incorrect_password(self,mock_bcrypt_using,mock_take_password,mock_verify_user_on_db):
        mock_verify_user_on_db.return_value.fetchall.return_value=[(1)]
        mock_take_password.return_value="Password"
        mock_verify_user_on_db.return_value.execute.return_value.fetchone.return_value="string"
        mock_bcrypt_using.return_value.verify.return_value=False
        with self.assertRaises(SystemExit) as cm:
              phonebook.read_db("John Doe")
        self.assertEqual(cm.exception.code,1)
    @patch('phonebook.verify_user_on_db')
    def test_user_not_found(self,mock_verify_user_on_db):
        mock_verify_user_on_db.return_value.fetchall.return_value=[]
        with self.assertRaises(SystemExit) as er:
            phonebook.read_db("fake user")
        self.assertEqual(er.exception.code,1)


    @classmethod
    def tearDownClass(cls) -> None:
        os.remove("test_phonebook.db")
        return super().tearDownClass()







if __name__=='__main__':
	unittest.main()