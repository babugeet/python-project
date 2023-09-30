# This is a sample project
# Revision history
# v2.1 babugeet;  Accepted password,hashed password, list db content after password check
# v2. babugeet; created db
# v1. babugeet; accepted input

import sqlite3
import os
from passlib.hash import bcrypt
from getpass import getpass

DB_NAME="C:/Users/babugeet/Documents/GitHub/python-project/phonebook.db"
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
    def __init__(self,input_dict):
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
                conn.close
    def read_db(self):
        conn = sqlite3.connect(DB_NAME) 
        c = conn.cursor()
        
        password = take_password()
        hashed_password=c.execute("SELECT PASS from phonebook WHERE NAme=(?)",(self.name,))
        # print(hashed_password.fetchone()[0])
        if self.hasher.verify(password, bytes(hashed_password.fetchone()[0],'utf-8')):
            c.execute("SELECT * from phonebook WHERE NAme=(?)",(self.name,))
            print(c.fetchall())
        else:
            print("Password Error")
        c.close()

create_db()
create_table()
phone_dict_content=take_input()
phone=PhoneBook(phone_dict)
phone.add_db()
phone.read_db()

# print(phone_dict_content)


