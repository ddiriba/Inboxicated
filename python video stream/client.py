#import json
import requests as req
import numpy
import os

#https://www.youtube.com/watch?v=GMppyAPbLYk&list=PLsY_JNR6SJpr3ilDfdMPU2Cv7KZV0urOF&index=3 
#
#client

#test image


with open('megan.png', 'rb') as TI:
    TESTIMAGE = TI.read()
    TESTIMAGE = TESTIMAGE.hex()

class SendData(object):
    def __init__(self):
        print("init client")
        #loopback address
        #self.BASE = "http://127.0.0.1:10050/"
        #John's server
        self.BASE = 'http://renoxdeception.duckdns.org:10050/'
        
    def send_dep_key(self):
        #ok/200 confirm
        response = req.put(self.BASE + "deposit_key/add_a_key", {"Name": "Test", "Phone" : "7758008918", "Index": "3", "Image": TESTIMAGE }) 
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
        response = req.put(self.BASE + "retrieve_key", {"image": TESTIMAGE})
        if response == 200:
            pass
        else:
            print('try again')
    
    def send_add_keeper(self):
        #ok/200 confirm
        response = req.put(self.BASE + "add_keeper", {"Name": "Test", "phone" : "7758008918", "password": "123"})
        if response == 200:
            pass
        else:
            print('try again')

def main():
    packet = SendData()
    packet.send_dep_key()


if __name__ == "__main__":
    main()

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

