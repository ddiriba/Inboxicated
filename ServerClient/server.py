'''
Client Features:
    Deposit Key
        ->name, phone, index, image,

    Retrieve Key
        ->image

    Add keeper
        ->name, phone, password?

    Summon Keeper
        ->?

    Submit Feedback
        -> long text


Server Features:
    Deposit Key
        <- 200 ok, confirm

    Retrieve Key
        <- name, index, drunk confidence

    Add Keeper
        <- 200 ok, confirm

    Submit Feedback
        <- 200 ok, confirm

'''

import os
import base64
from email.mime import image
import flask
from flask_restful import Api, Resource
import time
import DatabaseClass as DB

app = flask.Flask(__name__) #this would be replaced with app = flask.Flask(Inboxicated.py)/ flask.Flask(Inboxicated)
api = Api(app)

'''THE FUNCTIONS IN THIS CLASS SHOULD MAYBE RETURN THE VARIABLES, OR CALL THE DATABASE FOR ENTRY DIRECTLY'''
class DataGet(Resource):
    def __init__(self, name):
        self.i_db = DB.DataBase('inboxicated')
        #this location can changed but this will be where all faces will be stored
        if not os.path.exists('current_faces'):
            os.makedirs('current_faces')

    def put(self, command_type):
        if command_type =='test_conn':
            print("Test Successful")
            return 200
            
            
        if command_type == 'add_a_key':
            #first check the number of people already storing keys
            if self.i_db.getUserCount() > 6:
                return False, "All indexes are occupied"
            received_name = flask.request.form['Name']
            received_phone = flask.request.form['Phone']
            received_index = flask.request.form['Index']
            received_image = flask.request.form['Image']        
            writeTofile(received_image, ("current_faces/" +received_name+received_phone+".png")) #we should not be writing to file immediately
            recieved_user_id = 0 #maybe somethng random
            
            check_phone = self.i_db.retrieveAllUserPhones
            for i in self.i_db.retrieveAllUserPhones().values():
                if i == received_phone:
                    print('Phone Already Exists')
                    return False, "Phone Already Exists"

            self.i_db.insertUser(recieved_user_id, received_name, received_phone, received_index, received_image )

            #once all the checks have been done, it can 
            return {"name": received_name, "phone" : received_phone, "index": received_index}
            
        elif command_type == 'retrieve_key':
            received_image = flask.request.form['Image']
            self.i_db.retrieveUserFaces() #kinda pointless if we have a folder of faces already
            #facial recognition should be called here and use the folder created by the function
            t = time.localtime()
            currenttime = time.strftime("%m%d%Y%H%M%S", t)
            writeTofile(received_image, ("unknown" + currenttime + ".png"))

            
        elif command_type == 'add_keeper':
            received_name = flask.request.form['Name']
            received_phone = flask.request.form['Phone']
            received_password = flask.request.form['Password']
            print(received_name + ', you a keeper now')
        
        elif command_type == 'summon_keeper':
            keepers_dictionary = self.i_db.retrieveAllKeepers()
            return keepers_dictionary
        
        elif command_type == 'send_feedback':
            received_feedback = flask.request.form['Feedback']
            t = time.localtime()
            currenttime = time.strftime("%m%d%Y%H%M%S", t)
            nameoffile = ("FeedBack" + currenttime + ".txt")
            with open(nameoffile, 'w') as file:
                file.write(received_feedback)


api.add_resource(DataGet, "/inboxicated/<string:command_type>")

#turning the binary data column back to files
def writeTofile(byteimage, filename):
    
    #decode image from hex to byte array
    print(type(byteimage))
    byteimage = bytearray.fromhex(byteimage)
                
    #write image bytes to file
    with open(filename, 'wb') as file:
        file.write(byteimage)
    print("File ready : " +  filename)


#this starts the server
if __name__ == "__main__":
    #app.run(debug = True)
    
    #testing loopback address
    #host_val = "127.0.0.1"
    
    #john's pc
    host_val = "10.0.0.3"

    print(host_val)
    
    app.run(host = host_val, port = 10050, debug = True)
    #app.run(host = 'host_val', port = 10050) #this would be final implementation
