# This is a sample project
# Revision history
#TODO #18 Implement individual error message for password policy check
#TODO #10 Implement a admin password for deleting users
#TODO #8 Check if the user already exist before taking any more user input
#TODO #9 Supress unwanted message in log (when loglevel is DEBUG)
#TODO #7 Implement password policy check
# v2.5 babugeet; Added check for if the user already exist before taking any more user input; issue8
# v2.4 babugeet; Added password verification during add operation; issue#12
# v2.3 babugeet; Implemented Delete operation and password hidden
# v2.2 babugeet; Implemented argument approach for user input.
# v2.1 babugeet;  Accepted password,hashed password, list db content after password check
# v2. babugeet; created db
# v1. babugeet; accepted input

#Quick Info
# for editing db, open--> edit --> commit --> delete


import sqlite3
import os
import sys
import logging
import passlib.hash #import bcrypt
from getpass import getpass

from password_strength import PasswordPolicy

policy = PasswordPolicy.from_names(
    length=8,  # min length: 8
    uppercase=2,  # need min. 2 uppercase letters
    numbers=2,  # need min. 2 digits
    special=2,  # need min. 2 special characters
    nonletters=2,  # need min. 2 non-letter characters (digits, specials, anything)
)

DB_NAME="phonebook.db"
phone_dict={}
def create_db(dbname):
    if os.path.isfile(dbname):
        try:
            conn=sqlite3.connect(dbname)
            logging.info("db present")
            print("db present")
        except: 
            print("error in creating db")
            logging.error('error in creating db')
            exit()
def create_table(dbname):
    conn = sqlite3.connect(dbname) 
    c = conn.cursor()
    sql = 'create table if not exists phonebook (Name VARCHAR PRIMARY KEY, Age INT, Place VARCHAR, Phone INT, PASS VARCHAR)'
    c.execute(sql)
    conn.commit()
    conn.close()

def password_input(prompt):
    return getpass(prompt)

def password_policy_check(input):
    output=policy.test(input)
    if len(output)==0:
        pass
    else:
        print(output)
        exit(3)

def take_password():
    i=3
    #12 Ask password twice while collecting the password for add operation
    while i>=0:
        password = password_input("Enter the password: ")
        
        re_entered_pass = password_input("Re-enter the password: ")
        password_policy_check(re_entered_pass)
        if password==re_entered_pass:
            break
        else:
            i=i-1
        if i == 0:
            logging.error("Password check filled, user not added in the db")
            exit(2)
            

    return password

def verify_user_on_db(name_input):
    conn = sqlite3.connect(DB_NAME) 
    c = conn.cursor()
    c.execute("SELECT * from phonebook WHERE NAme=(?)",(name_input,))
    return c
        
def take_input():
    input_name=input("Enter your Name: ")
    #8 Check if the user already exist before taking any more user input
    c=verify_user_on_db(input_name)
    if len(c.fetchall()) != 0:
        print('duplicate {} user  found'.format(input_name))
        logging.error('duplicate {} user  found'.format(input_name))
        exit(1)
    phone_dict["name"]=input_name
    phone_dict["age"]=int(input("Enter your age: "))
    phone_dict["place"]=input("Enter your place: ")
    phone_dict["phone"]=int(input("Enter your phone number: "))
    password = take_password()
    print("Enter details to the active directory ")
    logging.info('Entering details to the active directory')
    # hashed_password = hasher.hash(password)
    phone_dict["password"]=password
    return phone_dict


class PhoneBook():
    def __init__(self,input_dict=None):
        self.name=input_dict["name"]
        self.age=input_dict["age"]
        self.place=input_dict["place"]
        self.phone=int(input_dict["phone"])
        self.hasher = passlib.hash.bcrypt.using(rounds=13) 
        self.password=self.hasher.hash(input_dict["password"])


    
    def add_db(self):
        conn = sqlite3.connect(DB_NAME) 
        c = conn.cursor()
        try:
            c.execute("INSERT INTO phonebook('Name','Age','Place','Phone','PASS') VALUES (?,?,?,?,?)",(self.name,self.age,self.place,self.phone,self.password))
            conn.commit()
            c.close()
        except sqlite3.Error as error:
            logging.error("Failed to insert data into sqlite table",error)
            print("Failed to insert data into sqlite table", error)
        finally:
            if conn:
                conn.close()
def read_db(name_input):
    c=verify_user_on_db(name_input)
    if len(c.fetchall()) == 0:
        print('{} user not found'.format(name_input))
        logging.error('{} user not found'.format(name_input))
        exit(1)
    password = take_password()
    hashed_password=c.execute("SELECT PASS from phonebook WHERE NAme=(?)",(name_input,)).fetchone()[0]
    # hasher = passlib.hash.bcrypt.using(rounds=13)
    flag=passlib.hash.bcrypt.using(rounds=13).verify(password, bytes(hashed_password,'utf-8'))
    # print(hashed_password.fetchone()[0])
    if flag:
        c.execute("SELECT NAme,Age,Place,Phone from phonebook WHERE NAme=(?)",(name_input,))
        output=c.fetchone()
        print(f'Name is {output[0]}, Age is {output[1]}, Place is {output[2]}, Phone number is {output[3]} ')
        logging.info(f'Output printed for user {output[0]}')
    else:
        print("Password Error")
        logging.error("Password Error")
        exit(1)
    c.close()

def operator_selection():
    if len(sys.argv) > 2:
        # print((sys.argv[0]))
        logging.error("Failed to recieve user input, multiple options given")
        print( " Only one operation supported at a time, pls choose one of ( add, read, delete)")
        exit(1)
    elif len(sys.argv)==1:
        logging.error("Failed to recieve user input, no options given")
        print( " No input arguments provided, pls choose one of ( add, read, delete)")
        exit(1)
    return sys.argv[1]

def delete_user(name_input):
    conn = sqlite3.connect(DB_NAME) 
    c = conn.cursor()
    print("Deleting {} from phonebook".format(name_input))
    logging.info("Deleting {} from phonebook".format(name_input))
    c.execute("delete  from phonebook where NAme=(?)",(name_input,))
    conn.commit()
    c.close()

def selection_execution(oper_input):
    if oper_input == "add":
        phone_dict_content=take_input()
        phone_diary=PhoneBook(phone_dict_content)
        phone_diary.add_db()
    elif oper_input =="read":
        name_input=input("Enter the name: ")
        read_db(name_input)
    elif oper_input=="delete":
        name_input=input("Enter the name of the user to be deleted: ")
        delete_user(name_input)
    else:
        print("wrong input choosen")
        logging.error("Failed to recieve user input, wrong options selected")
        exit(1)
    # match oper_input:
    #     case "add":
    #         phone_dict_content=take_input()
    #     case "read":
    #         pass:
    #     case "delete":
    #         pass
        

def main():
    logging.basicConfig(format='%(asctime)s %(message)s',filename='example.log', level=logging.DEBUG)
    create_db(DB_NAME)
    create_table(DB_NAME)
    oper_sel=operator_selection()
    selection_execution(oper_sel)
    

if __name__ == '__main__':
    main()