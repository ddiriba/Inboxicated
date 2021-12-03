import sqlite3

def main():
    
    command = "poo poo"
    #someone putting in their keys
    while command.upper() != "EXIT":
        command = input("what would you like to do (insert key, add keeper, get key) or 'exit' to end program")
        if command.upper() == "INSERT KEY":
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
            print("Which one of these people is you")
        else:
            print("Wrong command")
            
        db.showAll()


#going to be in a seperate file but will be imported
#all other stuff besides this class is just for testing purposes
class DataBase:
#Represent a sensor.
    def __init__(self, name):
        self.name = name
        conn = sqlite3.connect(self.name + '.db') 
        cursor = conn.cursor()
        
        cursor.execute('''
                  DROP TABLE IF EXISTS users
                  ''')
                  
        cursor.execute('''
                  DROP TABLE IF EXISTS keepers
                  ''')
                  
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
        
    def insertUser(self, user_id, user_name, user_phone, keyIndex, photo ):
        
        sqlite_insert_blob_query = """ INSERT INTO users
                                  (user_id, user_name, user_phone, user_number_tries, keyIndex, user_face) VALUES (?, ?, ?, ?, ?, ?)"""
        
        #make sure to format picture prior to inserting to database                  
        #user_face = self.convertToBinaryData(photo)
        user_face = photo
        
        data_tuple = (user_id, user_name, user_phone, 0 ,keyIndex, user_face)
        self.insertRecord(sqlite_insert_blob_query, data_tuple)


    
    def insertKeeper(self, keeper_id, keeper_name, Keeper_phone, master_keeper_flag, photo):
        sqlite_insert_blob_query = """ INSERT INTO keepers
                                  (keeper_id, keeper_name, Keeper_phone, master_keeper_flag, keeper_face) VALUES (?, ?, ?, ?, ?)"""
        
        #make sure to format picture prior to inserting to database                  
        #keeper_face = self.convertToBinaryData(photo)
        keeper_face = photo
        
        data_tuple = (keeper_id, keeper_name, Keeper_phone, master_keeper_flag, keeper_face)
        self.insertRecord(sqlite_insert_blob_query, data_tuple)
        
    def insertRecord(self, sqlite_insert_blob_query, data_tuple):
        try:
            conn = sqlite3.connect(self.name + '.db') 
            cursor = conn.cursor()
            cursor.execute(sqlite_insert_blob_query, data_tuple)
            conn.commit()
            print("You're in the box bud")
            cursor.close()
        except sqlite3.Error as error:
            print("Failed to add you in the box bud", error)
        finally:
            if conn:
                conn.close()
                print("connection closed")
        
    def removeUser(self,user_name, user_phone ):
        print(user_name)
        
    def retrieveUserFaces(self):
        print('here is your cute face')
              
    def showAll(self):
        conn = sqlite3.connect('inboxicated.db') 
        c = conn.cursor()
        sql_fetch_blob_query = "SELECT * from users"
        c.execute(sql_fetch_blob_query)
        record = c.fetchall()
        print(record)
        
        sql_fetch_blob_query = "SELECT * from keepers"
        c.execute(sql_fetch_blob_query)
        record = c.fetchall()
        print(record)
        conn.commit()
        if conn:
            conn.close()
            print("the sqlite connection is closed")
    

        
    def removeKeeper(self, keeper_name, Keeper_phone):
        print(keeper_name)
        
    def updateUserAttempts(self, user_name):
        print("you are drunk")
        
    def convertToBinaryData(self, filename):
    # Convert digital data to binary format
        with open(filename, 'rb') as file:
            blobData = file.read()
        return blobData



if __name__ == "__main__":
    db = DataBase('inboxicated')
    main() # kinda representing kivy running