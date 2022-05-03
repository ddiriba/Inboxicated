import face_recognition
import sqlite3
import os


def main():
    #for demonstration purpose only
    command = "test"
    #someone putting in their keys
    while command.upper() != "EXIT":
        command = input("Choose from one of the following options \n deposit key \n add keeper\n get key\n remove user \n remove keeper \n view all \n show faces (not fully testable) \n show phones \n get counts \n get facial encoding \n exit \n  ")
        if command.upper() == "DEPOSIT KEY":
            user_phone = input("Enter your phone: ")
            keyIndex = input("Enter where to store your keys: ")
            photo = input("Place your face here: ")
            #this represents all information grabbed from kivy gui
            db.insertUser(user_phone, keyIndex, photo)
            
        #someone adding a keeper    
        elif command.upper() == "ADD KEEPER":
            Keeper_phone = input("Enter your phone: ")
            keeper_password = input("Enter your password: ")   
            db.insertKeeper(Keeper_phone, keeper_password)
        elif command.upper() == "GET KEY":
            #query for all pictures to be shown
            #this would represent 
            user_name = input("Enter your name: ")
            user_phone = input("Enter your phone: ")
            db.updateUserAttempts(user_phone)
            print("Which one of these people is you")
        elif command.upper() == "REMOVE USER":
            phone = input("Enter your phone: ")
            db.removeRecord(phone, 'user')
        elif command.upper() == "REMOVE KEEPER":
            phone = input("Enter your phone: ")
            db.removeRecord(phone, 'keeper')
        elif command.upper() == "VIEW ALL":
            db.showAll()
        elif command.upper() == "SHOW FACES":
            print(db.retrieveUserFaces())
        elif command.upper() == "SHOW PHONES":
            print(db.retrieveAllUserPhones())
        elif command.upper() == "GET COUNTS":
            print(db.getUserCount())
        elif command.upper() == "GET FACIAL ENCODING":
            db.get_facial_encodings()        
        elif command.upper() == "GET INDEX":
            cheknum = input("Enter your phone: ")
            db.getUserIndex(cheknum)
        elif command.upper() == "GET PASS":
            diction = db.retrieveKeeperUserPass()
            print(diction)
            print(type(diction))
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
        #cursor.execute('''
        #                DROP TABLE IF EXISTS users
        #                ''')
                  
        #cursor.execute('''
        #                DROP TABLE IF EXISTS keepers
        #                  ''')

        #cursor.execute('''
        #                DROP TABLE IF EXISTS FeedBackLog
        #                  ''')     

        cursor.execute('''
                  CREATE TABLE IF NOT EXISTS users
                      ([user_phone] TEXT, 
                       [user_number_tries] INTEGER, 
                       [keyIndex] INTEGER,
                       [user_face] TEXT)
                  ''')
                  

        cursor.execute('''
                  CREATE TABLE IF NOT EXISTS keepers
                      ([Keeper_phone] TEXT, 
                       [Keeper_Password] TEXT)
                  ''')

        cursor.execute('''
                  CREATE TABLE IF NOT EXISTS FeedBackLog
                      ([IssueType] TEXT, 
                       [FeedBack] TEXT)
                  ''')

        conn.commit() 
        conn.close()
    
    def executeRecord(self, query, data_tuple):
        '''
        queries can be executed with generic formula by seperating them into
        a query and the data tuple that would fill in the conditions (where statmeents)
        '''
        result = None
        try:
            conn = sqlite3.connect(self.name + '.db') 
            cursor = conn.cursor()
            cursor.execute(query, data_tuple)
            conn.commit()
            print("Successful execution")
            result = cursor.fetchall()
            cursor.close()
        except sqlite3.Error as error:
            print("Failed execution", error)
            result = None
        finally:
            if conn:
                conn.close()
                print("connection closed")      
        return result #returns empty tuple on non-queries (update, delete)
    
    def insertUser(self, user_phone, keyIndex, photo ): 
        '''
        to store a user when a new key is deposited
        '''
        insert_query = """ INSERT INTO users
                                  (user_phone, user_number_tries, keyIndex, user_face) VALUES (?, ?, ?, ?)"""
        data_tuple = (user_phone, 0 ,keyIndex, photo)
        #[] indicates a successful query, None is returned on failed executions
        return self.executeRecord(insert_query, data_tuple) 

    def insertKeeper(self,  Keeper_phone, Keeper_Password): 
        '''
        to store a new keeper or additional keepers and their respective info
        '''
        insert_query = """ INSERT INTO keepers
                                  (Keeper_phone, Keeper_Password) VALUES (?, ?)"""
        data_tuple = ( Keeper_phone,  Keeper_Password)
        #[] indicates a successful query, None is returned on failed executions
        return self.executeRecord(insert_query, data_tuple)

    def insertFeedBack(self, IssueType, FeedBack):
        '''
        storing all logs/feedbacks/bugs that will be monitored by devs
        '''
        insert_query = """ INSERT INTO FeedBackLog
                                  (IssueType, FeedBack) VALUES (?, ?)""" 
        data_tuple =  (IssueType, FeedBack)
        #[] indicates a successful query, None is returned on failed executions
        return self.executeRecord(insert_query, data_tuple)    
        
    def removeRecord(self,  remove_id, user_type):
        '''
        when a user has retrieved their keys or when a keeper wants to 
        be removed from the database
        '''
        if user_type == 'user':
            remove_query = 'DELETE FROM users WHERE  user_phone =?'
        elif user_type == 'keeper':
            remove_query = 'DELETE FROM keepers WHERE Keeper_phone =?'
        else: #issue
            remove_query = 'DELETE FROM FeedBackLog WHERE FeedBack =?'
        data_tuple = (remove_id,)
        return self.executeRecord(remove_query, data_tuple)
        
    def retrieveUserFaces(self):
        '''
        retrieves the face encodings that are stored as hex in the db
        '''
        conn = sqlite3.connect('inboxicated.db') 
        c = conn.cursor()
        sql_fetch_insert_query = "SELECT user_phone, user_face FROM users"
        c.execute(sql_fetch_insert_query)
        record = c.fetchall()
        #should be an array of  phone numbers and face in hex/binary  
        if conn: #close connection 
            conn.close()
        return record

    def retrieveAllUserPhones(self):
        '''
        retrieves all user phone number that is utilized for
        override functionality which will ensure that a user exists
        in the list of phone numbers returned
        '''
        conn = sqlite3.connect('inboxicated.db') 
        c = conn.cursor()
        sql_fetch_insert_query = "SELECT  user_phone FROM users"
        c.execute(sql_fetch_insert_query)
        record = c.fetchall()
        #should be an array of  user_name  and user_phones
        phone_numbers = {}
        for i in record:
            phone_numbers[i[0]] = i[0] #fix this later, turn into list
        
        if conn: #close connection 
            conn.close()
        return phone_numbers

    def get_taken_indexes(self):
        '''
        retrieves all taken indexes inside the box to make sure there are 
        no overlapping storing of keys
        '''
        conn = sqlite3.connect('inboxicated.db') 
        c = conn.cursor()
        sql_fetch_insert_query = "SELECT  keyIndex FROM users"
        c.execute(sql_fetch_insert_query)
        record = c.fetchall()
        #should be an array of  user_name  and user_phones
        indexes = []
        for i in record:
            indexes.append(i[0])
        if conn: #close connection 
            conn.close()
        return indexes

    def retrieveAllKeepers(self): 
        '''
        function used to make sure that when a new keeper is added, they
        don't already exist in the database
        '''
        conn = sqlite3.connect('inboxicated.db') 
        c = conn.cursor()
        sql_fetch_insert_query = "SELECT keeper_phone FROM keepers"
        c.execute(sql_fetch_insert_query)
        record = c.fetchall()
        
        keepers_info = {}
        for i in record:
            keepers_info[i[0]] = i[0] 
        
        if conn: #close connection 
            conn.close()
        return keepers_info

    def retrieveKeeperUserPass(self): 
        '''
        retrieves all keepers when checking which credentials can
        be used to override an opening
        '''
        conn = sqlite3.connect('inboxicated.db') 
        c = conn.cursor()
        sql_fetch_insert_query = "SELECT keeper_phone,  Keeper_Password FROM keepers"
        c.execute(sql_fetch_insert_query)
        record = c.fetchall()
        #should be an array of  user_name  and user_phones
        keepers_user_pass = {}
        for i in record:
            keepers_user_pass[i[0]] = i[1]
        if conn: #close connection 
            conn.close()
        return keepers_user_pass

    def updateUserAttempts(self,  user_phone): 
        '''
        when a user is deemed intoxicated, their number of attempts will be incremented by 1,
        later utilized for sending a notifcation to the keepers that they have too many attempts
        '''
        print(user_phone)
        conn = sqlite3.connect(self.name + '.db') 
        cursor = conn.cursor()
        data_tuple = (user_phone,)
        sql_fetch_query = 'SELECT user_number_tries from users where  user_phone =?'
        #self.executeRecord()
        cursor.execute(sql_fetch_query, data_tuple)
        attempts = cursor.fetchall()
        attempt_value = attempts[0][0] #needs testing
        print(attempt_value)
        attempt_value += 1
        update_query = ''' UPDATE users
              SET user_number_tries = ? 
              WHERE user_phone =?'''
        data_tuple = (attempt_value, user_phone)
        cursor.execute(update_query, data_tuple)
        conn.commit()
        if conn:
            conn.close()
            print("the sqlite connection is closed")
        return attempt_value
    
    def getUserAttempts(self, user_phone):
        '''
        gets a user's number of attempt, making sure it's not greater than 3 (which means they've tried too many times)
        '''
        conn = sqlite3.connect(self.name + '.db') 
        cursor = conn.cursor()
        data_tuple = (user_phone)
        sql_fetch_query = 'SELECT user_number_tries from users where  user_phone =?'
        cursor.execute(sql_fetch_query, data_tuple)
        attempts = cursor.fetchall()
        attempt_value = attempts[0][0] #needs testing
        if conn:
            conn.close()
            print("the sqlite connection is closed")
        print(attempt_value)
        return attempt_value

    def getUserIndex(self, user_phone):
        '''
        gets user's info by using their phone number to see where they stored their keys
        '''
        conn = sqlite3.connect(self.name + '.db') 
        cursor = conn.cursor()
        data_tuple = (user_phone,)
        sql_fetch_query = 'SELECT keyIndex from users where  user_phone =?'
        cursor.execute(sql_fetch_query, data_tuple)
        index_found = cursor.fetchall()
        index_value = index_found[0][0] #needs testing
        if conn:
            conn.close()
            print("the sqlite connection is closed")
        print(index_value)
        return index_value

    def getUserCount(self):
        '''
        utilized to make sure the box is not already full when a user is trying to store their keys
        '''
        conn = sqlite3.connect('inboxicated.db') 
        c = conn.cursor()
        sql_fetch_insert_query = "SELECT COUNT(*) from users"
        c.execute(sql_fetch_insert_query)
        record = c.fetchall()
        
        if conn:
            conn.close()
        return record[0][0]

    def getKeeperCount(self):
        '''
        utilized to make sure there is at least one keeper before the application is started
        '''
        conn = sqlite3.connect('inboxicated.db') 
        c = conn.cursor()
        sql_fetch_insert_query = "SELECT COUNT(*) from keepers"
        c.execute(sql_fetch_insert_query)
        record = c.fetchall()
        if conn:
            conn.close()
        return record[0][0]

    def get_facial_encodings(self):
        '''
        utilizes the face_rec module to get face nencodings utilized by face recognition
        '''
        returned_record = self.retrieveUserFaces() #phone number, hex data
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
        '''
        helper function that decodes images from hex to byte arrays and writes it to a file
        '''
        byteimage = bytearray.fromhex(byteimage)
        #write image bytes to file
        with open('current_faces/' + filename, 'wb') as file:
            file.write(byteimage)

    #kept seperate on purpose, retrive method != deposit key
    def HexToArray(self, hex_byteimage, filename):
        '''
        helper function for file writer 
        '''
        self.writeTofile(hex_byteimage, filename)
        array_image = face_recognition.load_image_file("current_faces/" + filename)
        user_face_encoding = face_recognition.face_encodings(array_image)[0]
        return user_face_encoding
    
    def delete_db(self, name):
        '''
        mini deconstructor
        '''
        os.remove(name + '.db')
        print('deleted')
        return True
    #not needed simply for testing (maybe needed if there's app for the keepers)        
    def showAll(self):
        '''
        tessting funciton to display all info
        '''
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
        print('        Keeper_phone     |    Keeper_Password      ')
        for i in record:
            for j in i:
                offset = 18 - len(str(j))
                print(str(j) + ' ' * offset, end = ' | ')
            print('')
        if conn:
            conn.close()

if __name__ == "__main__":
    #has to be ran before kivy is launched
    #DB constructor in class
    db = DataBase('inboxicated') 
    main() # kinda representing kivy running
