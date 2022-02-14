import sqlite3

def main():
    #for demonstration purpose only
    command = "test"
    #someone putting in their keys
    while command.upper() != "EXIT":
        command = input("Choose from one of the following options \n deposit key \n add keeper\n get key\n remove user \n remove keeper \n view all \n show faces (not fully testable) \n show phones \n exit \n  ")
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
            db.retrieveUserFaces()
        elif command.upper() == "SHOW PHONES":
            db.retrieveAllUserPhones()
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
        
        #cursor.execute('''
        #          DROP TABLE IF EXISTS users
        #          ''')
                  
        #cursor.execute('''
        #          DROP TABLE IF EXISTS keepers
        #          ''')
                  
        cursor.execute('''
                  CREATE TABLE IF NOT EXISTS users
                      ([user_id] INTEGER PRIMARY KEY, 
                       [user_name] TEXT, 
                       [user_phone] TEXT, 
                       [user_number_tries] INTEGER, 
                       [keyIndex] INTEGER,
                       [user_face] TEXT)
                  ''')
                  
        cursor.execute('''
                  CREATE TABLE IF NOT EXISTS keepers
                      ([keeper_id] INTEGER PRIMARY KEY, 
                       [keeper_name] TEXT, 
                       [Keeper_phone] TEXT, 
                       [Master_keeper_flag] TEXT,
                       [keeper_face] TEXT)
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
    
    #potentially send this a tupple to the insertRecord rather than having 2 extra functions
    def insertUser(self, user_id, user_name, user_phone, keyIndex, photo ):
        insert_query = """ INSERT INTO users
                                  (user_id, user_name, user_phone, user_number_tries, keyIndex, user_face) VALUES (?, ?, ?, ?, ?, ?)"""
        #make sure to format picture prior to inserting to database                  
        #user_face = self.convertToBinaryData(photo)
        user_face = photo
        data_tuple = (user_id, user_name, user_phone, 0 ,keyIndex, user_face)
        self.executeRecord(insert_query, data_tuple)
    
    def insertKeeper(self, keeper_id, keeper_name, Keeper_phone, master_keeper_flag, photo):
        insert_query = """ INSERT INTO keepers
                                  (keeper_id, keeper_name, Keeper_phone, master_keeper_flag, keeper_face) VALUES (?, ?, ?, ?, ?)"""
        
        #make sure to format picture prior to inserting to database                  
        #keeper_face = self.convertToBinaryData(photo)
        keeper_face = photo
        
        data_tuple = (keeper_id, keeper_name, Keeper_phone, master_keeper_flag, keeper_face)
        self.executeRecord(insert_query, data_tuple)
                
    def removeRecord(self, name, phone, user_type):

            if user_type == 'user':
                remove_query = 'DELETE FROM users WHERE user_name =? and user_phone =?'
            else:#user
                remove_query = 'DELETE FROM keepers WHERE keeper_name=? and Keeper_phone =?'
            data_tuple = (name, phone)
            self.executeRecord(remove_query, data_tuple)
        
    def retrieveUserFaces(self):
        conn = sqlite3.connect('inboxicated.db') 
        c = conn.cursor()
        sql_fetch_insert_query = "SELECT user_name, user_face FROM users"
        c.execute(sql_fetch_insert_query)
        record = c.fetchall()
        #should be an array of  user_name  and user_face  
        for i in record:
            for j in i:
                #first j should be user name
                #second j should be user_face in binary data
                #self.writeTofile(data, filename):
                self.writeTofile(i[1], i[0])
        if conn: #close connection 
            conn.close()

    def retrieveAllUserPhones(self):
        conn = sqlite3.connect('inboxicated.db') 
        c = conn.cursor()
        sql_fetch_insert_query = "SELECT user_name,  user_phone FROM users"
        c.execute(sql_fetch_insert_query)
        record = c.fetchall()
        #should be an array of  user_name  and user_face  
        phone_numbers = {}
        for i in record:
            phone_numbers[i[0]] = i[1]
        print(phone_numbers)
        if conn: #close connection 
            conn.close()

    def updateUserAttempts(self, user_name, user_phone):
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

    # Convert digital data to binary format to store in db
    def convertToBinaryData(self, filename):
        with open(filename, 'rb') as file:
            blobData = file.read()
        return blobData

    #turning the binary data column back to files
    def writeTofile(self, data, filename):
        with open(filename, 'wb') as file:
            file.write(data)
        print("File ready : " +  filename)
        
        #not needed simply for testing (maybe needed if there's app for the keepers)        
    def showAll(self):
        conn = sqlite3.connect('inboxicated.db') 
        c = conn.cursor()
        sql_fetch_insert_query = "SELECT * from users"
        c.execute(sql_fetch_insert_query)
        record = c.fetchall()
        print('       user_id     |     user_name      |     user_phone     | user_number_tries  |      keyIndex      |     user_face    ')
        for i in record:
            for j in i:
                offset = 18 - len(str(j))
                print(str(j) + ' ' * offset, end = ' | ')
            print('')
        
        sql_fetch_insert_query = "SELECT * from keepers"
        c.execute(sql_fetch_insert_query)
        record = c.fetchall()
        print('\n\n')
        print('     keeper_id     |    keeper_name      |    Keeper_phone     | master_keeper_flag  |     keeper_face    ')
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
