# This is a sample project
# Revision history
#TODO implement delete operation
#TODO #1 remove printing of hashed password
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
from passlib.hash import bcrypt
from getpass import getpass

DB_NAME="phonebook.db"
phone_dict={}
def create_db():
    if os.path.isfile(DB_NAME):
        try:
            conn=sqlite3.connect(DB_NAME)
            print("db present")
        except: 
            print("error in creating db")
            exit()
def create_table():
    conn = sqlite3.connect(DB_NAME) 
    c = conn.cursor()
    sql = 'create table if not exists phonebook (Name VARCHAR PRIMARY KEY, Age INT, Place VARCHAR, Phone INT, PASS VARCHAR)'
    c.execute(sql)
    conn.commit()
    conn.close()

def take_password():
    password = getpass("Enter the password: ")
    return password
        
def take_input():

    print("Enter details to the active directory ")
    phone_dict["name"]=input("Enter your Name: ")
    phone_dict["age"]=int(input("Enter your age: "))
    phone_dict["place"]=input("Enter your place: ")
    phone_dict["phone"]=int(input("Enter your phone number: "))
    password = take_password()
    # hashed_password = hasher.hash(password)
    phone_dict["password"]=password
    return phone_dict


class PhoneBook():
    def __init__(self,input_dict=None):
        self.name=input_dict["name"]
        self.age=input_dict["age"]
        self.place=input_dict["place"]
        self.phone=int(input_dict["phone"])
        self.hasher = bcrypt.using(rounds=13) 
        self.password=self.hasher.hash(input_dict["password"])


    
    def add_db(self):
        conn = sqlite3.connect(DB_NAME) 
        c = conn.cursor()
        try:
            c.execute("INSERT INTO phonebook('Name','Age','Place','Phone','PASS') VALUES (?,?,?,?,?)",(self.name,self.age,self.place,self.phone,self.password))
            conn.commit()
            c.close()
        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)
        finally:
            if conn:
                conn.close()
def read_db(name_input):
    conn = sqlite3.connect(DB_NAME) 
    c = conn.cursor()
    c.execute("SELECT * from phonebook WHERE NAme=(?)",(name_input,))
    if len(c.fetchall()) == 0:
        print('{} user not found'.format(name_input))
        exit(1)
    password = take_password()
    hasher = bcrypt.using(rounds=13)
    hashed_password=c.execute("SELECT PASS from phonebook WHERE NAme=(?)",(name_input,))
    # print(hashed_password.fetchone()[0])
    if hasher.verify(password, bytes(hashed_password.fetchone()[0],'utf-8')):
        c.execute("SELECT NAme,Age,Place,Phone from phonebook WHERE NAme=(?)",(name_input,))
        print(c.fetchall())
    else:
        print("Password Error")
    c.close()

def operator_selection():
    if len(sys.argv) > 2:
        # print((sys.argv[0]))
        print( " Only one operation supported at a time, pls choose one of ( add, read, delete)")
        exit(1)
    return sys.argv[1]

def delete_user(name_input):
    conn = sqlite3.connect(DB_NAME) 
    c = conn.cursor()
    print("Deleting {} from phonebook".format(name_input))
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

    # match oper_input:
    #     case "add":
    #         phone_dict_content=take_input()
    #     case "read":
    #         pass:
    #     case "delete":
    #         pass
        

def main():
    create_db()
    create_table()
    oper_sel=operator_selection()
    selection_execution(oper_sel)
    

if __name__ == '__main__':
    main()