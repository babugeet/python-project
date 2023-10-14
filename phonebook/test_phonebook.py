import unittest
import os
import phonebook
import sqlite3

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
        stmt = "select * from phonebookr"
        try:
            c.execute(stmt)
        except sqlite3.OperationalError:
             self.fail("sql Table not found")
        result = c.fetchone()
        # print(result)
        self.assertIsNone(result, msg=None)

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove("test_phonebook.db")
        return super().tearDownClass()
    
if __name__=='__main__':
	unittest.main()