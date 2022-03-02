import os
import base64
#from email.mime import image
import flask
from flask_restful import Api, Resource
import time
import DatabaseClass as DB
from PIL import Image as im
import numpy as np
app = flask.Flask(__name__) #this would be replaced with app = flask.Flask(Inboxicated.py)/ flask.Flask(Inboxicated)
api = Api(app)


def writeTofile(byteimage, filename):
    #decode image from hex to byte array
    byteimage = bytearray.fromhex(byteimage)
    #write image bytes to file
    with open(filename, 'wb') as file:
        file.write(byteimage)

#kept seperate on purpose, retrive method != deposit key
def HexToArray(byteimage, filename):
    writeTofile(byteimage, filename)
    image = im.imread(filename)
    image_array =  np.asarray(image)
    return image_array



class DataGet(Resource):
    def __init__(self):
        self.i_db = DB.DataBase('inboxicated')
        #this location can changed but this will be where all faces will be stored
        if not os.path.exists('current_faces'):
            os.makedirs('current_faces')

    def put(self, command_type):
        if command_type =='test_conn':
            print("Test Successful")
            return 200
        elif command_type == 'check_for_keepers':
            num_of_keepers = self.i_db.getKeeperCount()
            return {"Master Check Response" : num_of_keepers}
        elif command_type == 'check_master':
            #check for master
            return True
        elif command_type == 'check_phone':
            received_phone = flask.request.form['Phone']
            print(str(received_phone))
            received_user_type = flask.request.form['UserType']
            print(received_user_type)
            print(str(received_user_type))
            if str(received_user_type) == 'U': #Check Types for User
                #first check the number of people already storing keys
                if self.i_db.getUserCount() > 6:
                    return {"Check Response" : "Box full"}

                for i in self.i_db.retrieveAllUserPhones().values():
                    if i == received_phone:
                        return {"Check Response" : "Phone Already Exists"}
                return {"Check Response" : "Proceed"}
            elif str(received_user_type) == 'K':
                print('entered')
                keeper_dict = self.i_db.retrieveAllKeepers()
                print(keeper_dict)
                for i in keeper_dict.values(): #returns dictionary of keeper and phones
                    print('passed :  ', end = '')
                    print(str(received_phone))
                    print('server :  ', end = '')
                    print(str(i))
                    if i == received_phone:
                        return {"Check Response" : "Phone Already Exists"}
                return {"Check Response" : "Proceed"}
        elif command_type == 'add_a_key':
            received_name = flask.request.form['Name']
            received_phone = flask.request.form['Phone']
            received_index = flask.request.form['Index']
            received_image = flask.request.form['Image'] #image stored in db as hex data
            recieved_user_id = 0 #maybe somethng random
            self.i_db.insertUser(recieved_user_id, received_name, received_phone, received_index, received_image)
            return {"Deposit Response" : "Successful Deposit"}
        elif command_type == 'retrieve_key':
            received_image_byte = flask.request.form['Image']
            writeTofile(received_image_byte, 'Unknown.png')
            imgae_to_array = im.open('Unknown.png')
            numpy_image = np.asarray(imgae_to_array)

            #facial recognition is called here with numpy_image

            faces_and_names = self.i_db.retrieveUserFaces()
            face_encodings = []
            face_names = []
            for i in faces_and_names:
                for j in i:
                    #first j should be user name
                    #second j should be user_face in hex data
                    face_encodings.append(HexToArray(i[1], i[0] + '.png'))
                    face_names.append( i[0])
            print(face_names)
            
            #note to DAWIT, need to implmenet delete file function to remove images after facerec
            #face congition class can be called now with face_encodings and face_names as the constructor parameters
            #face_recognize function from face recognition can be called with numpy_image as parameter

            #recognized face would be returned as a string and replace 'test_name'
            return {"recognized_face" : "test_name"}

        elif command_type == 'add_keeper':
            recieved_id = 69 #not implemented on app
            received_name = flask.request.form['Name']
            received_master_flag = '0' #not implemented on app
            received_phone = flask.request.form['Phone']
            recieved_username = 'fake_user_name' #not implemented on app
            received_password = flask.request.form['Password']
            recieved_face = ''
            self.i_db.insertKeeper(recieved_id, received_name, received_phone, received_master_flag, recieved_username, received_password,  recieved_face)
            print(str(received_name) + ', you a keeper now')
            #check keeper phones here
            return {"Keeper Response" : "Success"}

        elif command_type == 'get_keeper_password':
            dict_keeper_pass = self.i_db.retrieveKeeperUserPass()
            return {"Keeper Passwords" : dict_keeper_pass }
        elif command_type == 'summon_keeper':
            keepers_dictionary = self.i_db.retrieveAllKeepers()
            return keepers_dictionary
        elif command_type == 'send_feedback':
            received_Type = flask.request.form['Type']
            received_feedback = flask.request.form['Feedback']
            self.i_db.insertFeedBack(received_Type, received_feedback)


api.add_resource(DataGet, "/inboxicated/<string:command_type>")







#this starts the server
if __name__ == "__main__":
    #app.run(debug = True)
    
    #testing loopback address
    host_val = "127.0.0.1"
    
    #john's pc
    #host_val = "10.0.0.3"

    print(host_val)
    
    app.run(host = host_val, port = 10050, debug = True)
    #app.run(host = 'host_val', port = 10050) #this would be final implementation
