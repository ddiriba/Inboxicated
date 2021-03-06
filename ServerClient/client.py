import requests as req
from PIL import Image as im
import json
#https://www.youtube.com/watch?v=GMppyAPbLYk&list=PLsY_JNR6SJpr3ilDfdMPU2Cv7KZV0urOF&index=3 

#client

'''
SEND DATA OBJECT, THIS CLASS NEEDS THE ABILITY TO ADD JSON DATA TO ITS ARGUMENTS, BUT RIGHT NOW CALLING THE SUBFUNCTION WORKS. 
'''
class SendData(object):
    def __init__(self):
        #loopback address
        #self.BASE = "http://127.0.0.1:10050/"

        #John's server
        self.BASE = 'http://renoxdeception.duckdns.org:10050/'
        
    def send_init_test(self):
        '''
        testing initially before starting application
        '''
        try:
            response = req.put(self.BASE + "inboxicated/test_conn", timeout=2) 
            print(response)
            if response.status_code == 200:
                return True
            else:
                return False
        except:
            return False
     
    def check_for_master(self):
        '''
        front end fucntion to be utilized by getting number of keepers in the db
        '''
        try:
            response = req.put(self.BASE + "inboxicated/check_for_keepers") 
            if response.status_code == 200:
                return response.json()['Master Check Response'] #returns either 'Phone Already Exists' or 'Success' 
            else:
                return 'Server Down'
        except:
            return 'Server Issue'

    def send_dep_key(self, phone, index, image):
        '''
        front end function to be utilized to store all user information recorded
        '''
        try:
            #ok/200 confirm
            response = req.put(self.BASE + "inboxicated/add_a_key", { "Phone" : phone, "Index": index, "Image": image }) 
            if response.status_code == 200:
                return response.json()['Deposit Response'] #returns either 'Phone Already Exists' or 'Success' 
            else:
                return 'Server Down'
        except:
            return 'Server Issue'

    def get_keeper_passwords(self):
        '''
        front end function to be utilized for getting credentials that can be used to override
        '''
        try:
            response = req.put(self.BASE + "inboxicated/get_keeper_password") 
            if response.status_code == 200:
                return_dic = json.loads(response.json()['Keeper Passwords'])
                print(return_dic)
                print(type(return_dic))
                return return_dic #returns either 'Phone Already Exists' or 'Success' 
            else:
                return 'Server Down'
        except:
            return 'Server Issue'

    def check_user_phone(self, phone):
        '''
        front end function to be utilized for checking if user already exists in database
        '''
        try:
            response = req.put(self.BASE + "inboxicated/check_phone", {"Phone" : phone, "UserType": 'U'}) 
            if response.status_code == 200:
                return response.json()['Check Response'] #returns either 'Phone Already Exists' or 'Proceed' or 'Box Full'
            else:
                return 'Server Down'
        except:
            return 'Server Issue'

    def check_keeper_phone(self, phone):
        '''
        front end function to be utilized for checking if keeper is already exists in database
        '''
        try:
            response = req.put(self.BASE + "inboxicated/check_phone", {"Phone" : phone, "UserType": 'K'}) 
            if response.status_code == 200:
                return response.json()['Check Response'] #returns either 'Phone Already Exists' or 'Proceed' 
            else:
                return 'Server Down'
        except:
            return 'Server Issue'

    def send_ret_key(self, image_array):
        '''
        front end function to be utilized by sending image hex data to perform face recognition
        '''
        try:
            image = self.arrayToHex(image_array)
            response = req.put(self.BASE + "inboxicated/retrieve_key", {"Image": image})
            if response.status_code == 200:
                print(response.json())
                #need to add conition for unregonized face
                return response.json()['recognized_face']
            else:
                return 'Server Down'
        except:
            return 'Server Issue'

    def send_ret_index(self, user_phone):
        '''
        front end function to retrieve user box index based on phone number
        '''
        try:
            response = req.put(self.BASE + "inboxicated/retrieve_index", {"Phone" : user_phone})
            if response.status_code == 200:
                print(response.json())
                #need to add conition for unregonized face
                return response.json()['user_db_index']
            else:
                return 'Server Down'
        except:
            return 'Server Issue'
   
    def send_add_keeper(self, phone,  password):
        '''
        front end function to store new keeper info
        '''
        try:
            response = req.put(self.BASE + "inboxicated/add_keeper", { "Phone" : phone, "Password":password})

            if response.status_code == 200:
                return response.json()['Keeper Response']
            else:
                return 'Server Down'
        except:
            return 'Server Issue'

    def send_feedback(self, type, issue_text):
        '''
        front end function to store feed back logs
        '''
        try:
            response = req.put(self.BASE + "inboxicated/send_feedback", {"Type": type, "Feedback":issue_text})
            if response.status_code == 200:
                return response.json()['Feedback Response']
            else:
                return 'Server Down'
        except:
            return 'Server Issue'

    def send_notification(self):
        '''
        front end function to perform SMS notifcation
        '''
        try:
            response = req.put(self.BASE + "inboxicated/summon_keeper")
            if response.status_code == 200:
                return response.json()['Notification Response']
            else:
                return 'Server Down'
        except:
            return 'Server Issue'
    
    def send_update_attempts(self, phone_num):
        '''
        front end function to update user's number of attempts at opening box
        '''
        try:
            print(phone_num)
            response = req.put(self.BASE + "inboxicated/update_attempts", {"Phone": phone_num})
            if response.status_code == 200:
                return response.json()['Attempt Response']
            else:
                return 'Server Down'
        except:
            return 'Server Issue'

    ''' Helper Functions '''
    def arrayToHex(self, array):
        '''
        changing image to array and to hex data prior to storing/sending to server db
        '''
        try:
            #turning the array data to files        
            picture_data = im.fromarray(array)
            picture_data.save("unknown.png")
            return self.file_to_hex("unknown.png")
        except:
            return 'Byte Conversion Error'
            

    def file_to_hex(self, file_name):
        '''
        changing image to hex data prior to sending to server
        '''
        try:
            with open(file_name, 'rb') as TI:
                ByteData = TI.read()
                #convert image to hex
                Hexdata = ByteData.hex()
                return Hexdata
            
        except:
            print('hex NOT converted')
            return 'Hex Conversion Error'
            
            

def main():
    '''
    testing only
    '''
    
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



