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

#https://www.youtube.com/watch?v=GMppyAPbLYk&list=PLsY_JNR6SJpr3ilDfdMPU2Cv7KZV0urOF&index=3 
#
#client

#test image

'''
IMAGE IS ACCEPTED HERE, MUST BE CONVERTED FROM BYTES TO HEX, PERHAPS MAKE THIS A FUNCTION OF THE CLASS
'''
with open('megan.png', 'rb') as TI:
    TESTIMAGE = TI.read()
    #convert image to hex
    TESTIMAGE = TESTIMAGE.hex()


'''
SEND DATA OBJECT, THIS CLASS NEEDS THE ABILITY TO ADD JSON DATA TO ITS ARGUMENTS, BUT RIGHT NOW CALLING THE SUBFUNCTION WORKS. 
'''
class SendData(object):
    def __init__(self):
        print("init client")
        #loopback address
        #self.BASE = "http://127.0.0.1:10050/"
        #John's server
        self.BASE = 'http://renoxdeception.duckdns.org:10050/'
        
    def send_dep_key(self):
        #ok/200 confirm
        response = req.put(self.BASE + "inboxicated/add_a_key", {"Name": "Harambe", "Phone" : "7758008555", "Index": "3", "Image": TESTIMAGE }) 
        #response = req.put(self.BASE + "deposit_key/add_a_key", {"Name": "Test", "Phone" : "7758008918", "Index": "3"}) 

        #response = req.put(self.BASE + "deposit_key")
        #print(TESTIMAGE)
        
        #response = req.put(self.BASE + "deposit_key")
        print(response.json())
        if response == 200:
            pass
        else:
            print('try again')

    def send_ret_key(self):
        #ok/200 confirm
        response = req.put(self.BASE + "inboxicated/retrieve_key", {"Image": TESTIMAGE})
        if response != 200:
            print('try again')
        else:
            pass
    
    def send_add_keeper(self):
        #ok/200 confirm
        response = req.put(self.BASE + "inboxicated/add_keeper", {"Name": "Harambe", "Phone" : "7758008555", "Password": "123"})
        if response == 200:
            pass
        else:
            print('try again')
    def send_feedback(self):
        #ok/200 confirm
        response = req.put(self.BASE + "inboxicated/send_feedback", {"Feedback": "This is some long text to prove that it's working"})
        if response == 200:
            pass
        else:
            print('try again')

def main():
    packet = SendData()
    packet.send_dep_key()
    packet.send_ret_key()
    packet.send_add_keeper()
    packet.send_feedback()


if __name__ == "__main__":
    main()



