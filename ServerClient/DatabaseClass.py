import face_recognition
import sqlite3
import io
import numpy as np
from PIL import Image as im
def main():
    #for demonstration purpose only
    command = "test"
    #someone putting in their keys
    while command.upper() != "EXIT":
        command = input("Choose from one of the following options \n deposit key \n add keeper\n get key\n remove user \n remove keeper \n view all \n show faces (not fully testable) \n show phones \n get counts \n get facial encoding \n exit \n  ")
        if command.upper() == "DEPOSIT KEY":
            user_id = input("Enter your user id: ")
            user_name = input("Enter your name: ")
            user_phone = input("Enter your phone: ")
            keyIndex = input("Enter where to store your keys: ")
            photo = input("Place your face here: ")
            #this represents all information grabbed from kivy gui
            db.insertUser(user_id, user_name, user_phone, keyIndex, photo)
            
        #someone adding a keeper    
        elif command.upper() == "ADD KEEPER":
            keeper_id = input("Enter the keeper's id: ")
            keeper_name = input("Enter your name: ")
            Keeper_phone = input("Enter your phone: ")
            master_keeper_flag = input("Enter your flag: ")   
            photo = input("show me your face: ")   
            db.insertKeeper( keeper_id, keeper_name, Keeper_phone, master_keeper_flag, photo)
        elif command.upper() == "GET KEY":
            #query for all pictures to be shown
            #this would represent 
            user_name = input("Enter your name: ")
            user_phone = input("Enter your phone: ")
            db.updateUserAttempts(user_name, user_phone)
            print("Which one of these people is you")
        elif command.upper() == "REMOVE USER":
            name = input("Enter your name: ")
            phone = input("Enter your phone: ")
            db.removeRecord(name, phone, 'user')
        elif command.upper() == "REMOVE KEEPER":
            name = input("Enter your name: ")
            phone = input("Enter your phone: ")
            db.removeRecord(name, phone, 'keeper')
        elif command.upper() == "VIEW ALL":
            db.showAll()
        elif command.upper() == "SHOW FACES":
            print(db.retrieveUserFaces())
        elif command.upper() == "SHOW PHONES":
            print(db.retrieveAllUserPhones())
            for i in db.retrieveAllUserPhones().values():
                if i == '8985056666':
                    print('duplicate found')
        elif command.upper() == "GET COUNTS":
            print(db.getUserCount())
        elif command.upper() == "GET FACIAL ENCODING":
            db.get_facial_encodings()        
        else:
            print("Wrong command")
            
        

#going to be in a seperate file but will be imported
#all other stuff besides this class is just for testing purposes
class DataBase:
#Represent a sensor.
    def __init__(self, name):
        self.name = name
        conn = sqlite3.connect(self.name + '.db') 
        cursor = conn.cursor()
        
        #uncomment these to modify table structure
        cursor.execute('''
                  DROP TABLE IF EXISTS users
                      ''')
                  
        cursor.execute('''
                        DROP TABLE IF EXISTS keepers
                          ''')

        cursor.execute('''
                        DROP TABLE IF EXISTS FeedBackLog
                          ''')
                  
        cursor.execute('''
                  CREATE TABLE IF NOT EXISTS old_users
                      ([user_id] INTEGER PRIMARY KEY, 
                       [user_name] TEXT, 
                       [user_phone] TEXT, 
                       [user_number_tries] INTEGER, 
                       [keyIndex] INTEGER,
                       [user_face] TEXT)
                  ''')

        cursor.execute('''
                  CREATE TABLE IF NOT EXISTS users
                      ([user_phone] TEXT, 
                       [user_number_tries] INTEGER, 
                       [keyIndex] INTEGER,
                       [user_face] TEXT)
                  ''')
                  
        cursor.execute('''
                  CREATE TABLE IF NOT EXISTS old_keepers
                      ([keeper_id] INTEGER PRIMARY KEY, 
                       [keeper_name] TEXT, 
                       [Keeper_phone] TEXT, 
                       [Master_keeper_flag] TEXT,
                       [Keeper_UserName] TEXT,
                       [Keeper_Password] TEXT,
                       [keeper_face] TEXT)
                  ''')

        cursor.execute('''
                  CREATE TABLE IF NOT EXISTS keepers
                      ([Keeper_phone] TEXT, 
                       [Keeper_Password] TEXT,
                       [keeper_face] TEXT)
                  ''')

        cursor.execute('''
                  CREATE TABLE IF NOT EXISTS FeedBackLog
                      ([IssueType] TEXT, 
                       [FeedBack] TEXT)
                  ''')

        conn.commit() 
    
    def executeRecord(self, insert_query, data_tuple):
        try:
            conn = sqlite3.connect(self.name + '.db') 
            cursor = conn.cursor()
            cursor.execute(insert_query, data_tuple)
            conn.commit()
            print("Successful execution")
            cursor.close()
        except sqlite3.Error as error:
            print("Failed execution", error)
        finally:
            if conn:
                conn.close()
                print("connection closed")    
    
    def insertUser(self, user_id, user_name, user_phone, keyIndex, photo ): #remove extra columns
        insert_query = """ INSERT INTO users
                                  (user_id, user_name, user_phone, user_number_tries, keyIndex, user_face) VALUES (?, ?, ?, ?, ?, ?)"""
        user_face = photo
        data_tuple = (user_id, user_name, user_phone, 0 ,keyIndex, user_face)
        self.executeRecord(insert_query, data_tuple)

    def insertKeeper(self, keeper_id, keeper_name, Keeper_phone, Master_keeper_flag, Keeper_UserName, Keeper_Password,  keeper_face): #remove extra columns
        insert_query = """ INSERT INTO keepers
                                  (keeper_id, keeper_name, Keeper_phone, master_keeper_flag, Keeper_UserName, Keeper_Password, keeper_face) VALUES (?, ?, ?, ?, ?, ?, ?)"""
        data_tuple = (keeper_id, keeper_name, Keeper_phone, Master_keeper_flag, Keeper_UserName, Keeper_Password,  keeper_face)
        self.executeRecord(insert_query, data_tuple)

    def insertFeedBack(self, IssueType, FeedBack):
        insert_query = """ INSERT INTO FeedBackLog
                                  (IssueType, FeedBack) VALUES (?, ?)""" 
        data_tuple =  (IssueType, FeedBack)
        self.executeRecord(insert_query, data_tuple)    
        
    def removeRecord(self, name, phone, user_type): #change to phone number
            if user_type == 'user':
                remove_query = 'DELETE FROM users WHERE user_name =? and user_phone =?'
            else:#keeper
                remove_query = 'DELETE FROM keepers WHERE keeper_name=? and Keeper_phone =?'
            data_tuple = (name, phone)
            self.executeRecord(remove_query, data_tuple)
        
    def retrieveUserFaces(self):
        conn = sqlite3.connect('inboxicated.db') 
        c = conn.cursor()
        sql_fetch_insert_query = "SELECT user_phone, user_face FROM users"
        c.execute(sql_fetch_insert_query)
        record = c.fetchall()
        #should be an array of  phone numbers and face in hex/binary  
        if conn: #close connection 
            conn.close()
        return record

    def retrieveAllUserPhones(self): #remove names, change dictionary to list
        conn = sqlite3.connect('inboxicated.db') 
        c = conn.cursor()
        sql_fetch_insert_query = "SELECT user_name,  user_phone FROM users"
        c.execute(sql_fetch_insert_query)
        record = c.fetchall()
        #should be an array of  user_name  and user_phones
        phone_numbers = {}
        for i in record:
            phone_numbers[i[0]] = i[1]
        
        if conn: #close connection 
            conn.close()
        return phone_numbers

    def retrieveAllKeepers(self): #remove name, change dictionary to list
        conn = sqlite3.connect('inboxicated.db') 
        c = conn.cursor()
        sql_fetch_insert_query = "SELECT keeper_name,  keeper_phone FROM keepers"
        c.execute(sql_fetch_insert_query)
        record = c.fetchall()
        #should be an array of  user_name  and user_phones
        keepers_info = {}
        for i in record:
            keepers_info[i[0]] = i[1]
        
        if conn: #close connection 
            conn.close()
        return keepers_info

    def retrieveKeeperUserPass(self): #remove name, change dictionary to list
        conn = sqlite3.connect('inboxicated.db') 
        c = conn.cursor()
        sql_fetch_insert_query = "SELECT Keeper_UserName,  Keeper_Password FROM keepers"
        c.execute(sql_fetch_insert_query)
        record = c.fetchall()
        #should be an array of  user_name  and user_phones
        keepers_user_pass = {}
        for i in record:
            keepers_user_pass[i[0]] = i[1]
        if conn: #close connection 
            conn.close()
        return keepers_user_pass

    def updateUserAttempts(self, user_name, user_phone): #change to phone only
        conn = sqlite3.connect(self.name + '.db') 
        cursor = conn.cursor()
        data_tuple = (user_name, user_phone)
        sql_fetch_query = 'SELECT user_number_tries from users where user_name =? and user_phone =?'
        cursor.execute(sql_fetch_query, data_tuple)
        attempts = cursor.fetchall()
        for i in attempts:
            for j in i:
                attempts = j
        print(j)
        if attempts < 3:
            attempts += 1
        else:
            #alert the keeper
            attempts = 0 #reset maybe?
            print('Im calling the cops')
        update_query = ''' UPDATE users
              SET user_number_tries = ? 
              WHERE  user_name =? and user_phone =?'''
        data_tuple = (attempts, user_name, user_phone)
        cursor.execute(update_query, data_tuple)
        conn.commit()
        if conn:
            conn.close()
            print("the sqlite connection is closed")

    def getUserCount(self):
        conn = sqlite3.connect('inboxicated.db') 
        c = conn.cursor()
        sql_fetch_insert_query = "SELECT COUNT(*) from users"
        c.execute(sql_fetch_insert_query)
        record = c.fetchall()
        
        if conn:
            conn.close()
        return record[0][0]

    def getKeeperCount(self):
        conn = sqlite3.connect('inboxicated.db') 
        c = conn.cursor()
        sql_fetch_insert_query = "SELECT COUNT(*) from keepers"
        c.execute(sql_fetch_insert_query)
        record = c.fetchall()

    def get_facial_encodings(self):
        returned_record = self.retrieveUserFaces() #phone number, hex data
        #print("Returned from database:", returned_record)
        print("of type: ", type(returned_record))
        for i in returned_record:
            for j in i:
                print("tuple type: ", type(j))
        facial_encoded_dictionary = {}
        for i in returned_record: 
            array_format = self.HexToArray(i[1], i[0])
            facial_encoded_dictionary[i[0]] = array_format
        return facial_encoded_dictionary

    #helper functions 
    def writeTofile(self, byteimage, filename):
        #decode image from hex to byte array
        byteimage = bytearray.fromhex(byteimage)
        #write image bytes to file
        with open('current_faces/' + filename, 'wb') as file:
            file.write(byteimage)

    #kept seperate on purpose, retrive method != deposit key
    def HexToArray(self, hex_byteimage, filename): #takes hex, phonenumber
        self.writeTofile(hex_byteimage, filename)
        array_image = face_recognition.load_image_file("current_faces/" + filename)
        user_face_encoding = face_recognition.face_encodings(array_image)[0]
        return user_face_encoding
       
    #not needed simply for testing (maybe needed if there's app for the keepers)        
    def showAll(self):
        conn = sqlite3.connect('inboxicated.db') 
        c = conn.cursor()
        sql_fetch_insert_query = "SELECT * from users"
        c.execute(sql_fetch_insert_query)
        record = c.fetchall()
        print('       user_phone     | user_number_tries  |      keyIndex      |     user_face    ')
        for i in record:
            for j in i:
                offset = 18 - len(str(j))
                print(str(j) + ' ' * offset, end = ' | ')
            print('')
        
        sql_fetch_insert_query = "SELECT * from keepers"
        c.execute(sql_fetch_insert_query)
        record = c.fetchall()
        print('\n\n')
        print('       keeper_name      |    Keeper_phone     |    Keeper_Password    |    keeper_face    ')
        for i in record:
            for j in i:
                offset = 18 - len(str(j))
                print(str(j) + ' ' * offset, end = ' | ')
            print('')
        if conn:
            conn.close()
        return record[0][0]
if __name__ == "__main__":
    #has to be ran before kivy is launched
    #DB constructor in class
    db = DataBase('inboxicated') 
    main() # kinda representing kivy running
