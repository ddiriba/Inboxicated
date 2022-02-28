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

#import json
import requests as req
import numpy
import os
from PIL import Image as im
#https://www.youtube.com/watch?v=GMppyAPbLYk&list=PLsY_JNR6SJpr3ilDfdMPU2Cv7KZV0urOF&index=3 
#
#client

#test image




'''
SEND DATA OBJECT, THIS CLASS NEEDS THE ABILITY TO ADD JSON DATA TO ITS ARGUMENTS, BUT RIGHT NOW CALLING THE SUBFUNCTION WORKS. 
'''
class SendData(object):
    def __init__(self):
        #print("init client")
        #loopback address
        self.BASE = "http://127.0.0.1:10050/"
        #John's server
        #self.BASE = 'http://renoxdeception.duckdns.org:10050/'
        
        #get current filled indices
    
    def send_init_test(self):
        response = req.put(self.BASE + "inboxicated/test_conn", timeout=2) 
        print(response)
        if response.status_code == 200:
            return True
        else:
            return False
        
    def send_dep_key(self, name, phone, index, image):
        #ok/200 confirm
        response = req.put(self.BASE + "inboxicated/add_a_key", {"Name": name, "Phone" : phone, "Index": index, "Image": image }) 
        if response.status_code == 200:
            return response.json()['Deposit Response'] #returns either 'Phone Already Exists' or 'Success' 
        else:
            return 'Server Issue'

    def get_keeper_passwords(self):
        response = req.put(self.BASE + "inboxicated/get_keeper_password", { "UserType": 'U'}) 
        if response.status_code == 200:
            return response.json()['Keeper Passwords'] #returns either 'Phone Already Exists' or 'Success' 
        else:
            return {'500': 'Server Issue'}

    def check_user_phone(self, phone):
        response = req.put(self.BASE + "inboxicated/check_phone", {"Phone" : phone, "UserType": 'U'}) 
        if response.status_code == 200:
            return response.json()['Check Response'] #returns either 'Phone Already Exists' or 'Proceed' or 'Box Full'
        else:
            return 'Server Issue'
    def check_keeper_phone(self, phone):
        response = req.put(self.BASE + "inboxicated/check_phone", {"Phone" : phone, "UserType": 'K'}) 
        if response.status_code == 200:
            return response.json()['Check Response'] #returns either 'Phone Already Exists' or 'Proceed' 
    def send_ret_key(self, image_array):
        #ok/200 confirm+
        print(image_array.shape)
        image = self.arrayToHex(image_array)
        response = req.put(self.BASE + "inboxicated/retrieve_key", {"Image": image})
        if response.status_code == 200:
            print(response.json())
            #need to add conition for unregonized face
            return response.json()['recognized_face']
        else:
            return 'Server Issue'#this can be changed to either send into constant loop or just to close pop up, for now we are pretending everything is perfect

    
    def send_add_keeper(self, name, phone,  password):
        password = 124 #temporary until user and password are implemented
        #ok/200 confirm
        response = req.put(self.BASE + "inboxicated/add_keeper", {"Name": name, "Phone" : phone, "Password":password})

        if response.status_code == 200:
            return response.json()['Keeper Response']
        else:
            return 'Server Issue'

    def send_feedback(self, type, issue_text):
        #ok/200 confirm
        response = req.put(self.BASE + "inboxicated/send_feedback", {"Type": type, "Feedback":issue_text})
        if response.status_code == 200:
            return response.json()['Keeper Response']
        else:
            return 'Server Issue'

    #helper functions
    def arrayToHex(self, array):
        #turning the array data to files        
        print(array.shape) #testing purposes
        picture_data = im.fromarray(array)
        picture_data.save("unknown.png")
        return self.file_to_hex("unknown.png")

    def file_to_hex(self, file_name):
        with open(file_name, 'rb') as TI:
            ByteData = TI.read()
            #convert image to hex
            Hexdata = ByteData.hex()
            return Hexdata
            

def main():
    
    '''
    IMAGE IS ACCEPTED HERE, MUST BE CONVERTED FROM BYTES TO HEX, PERHAPS MAKE THIS A FUNCTION OF THE CLASS
    '''
    with open('megan.png', 'rb') as TI:
        TESTIMAGE = TI.read()
        #convert image to hex
        TESTIMAGE = TESTIMAGE.hex()
    
    packet = SendData()
    packet.send_dep_key()
    packet.send_ret_key(TESTIMAGE)
    packet.send_add_keeper()
    packet.send_feedback()


if __name__ == "__main__":
    main()



