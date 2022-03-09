import unittest as u
import DatabaseClass as DB
from server import DataGet, Run_App
from client import SendData
import PictureFaceRecognition as pfr
import os

#component testing
class TestClient(u.TestCase):
    def test_check_for_master(self):
        test_client = SendData()
        self.assertEqual(test_client.check_for_master(), 'Server Issue')

    # functions to test for DB
    '''
    def writeTofile(self, byteimage, filename):
    def HexToArray(self, hex_byteimage, filename):
    def getKeeperCount(self):
    def getUserCount(self):
    def get_facial_encodings(self):
    def updateUserAttempts(self,  user_phone): 
    def retrieveKeeperUserPass(self):
    def retrieveAllKeepers(self): 
    def retrieveUserFaces(self):
    def retrieveAllUserPhones(self):

    '''
class TestDatabase(u.TestCase):
    def test_execution(self):
        test_DB = DB.DataBase('test')
        query = ' SELECT keeper_phone FROM keepers WHERE keeper_phone = ?'
        data_tuple = ('775000000',)
        #empty tuple indicates a successful query, None is returned on failed executions
        self.assertEqual(test_DB.executeRecord(query, data_tuple), [])

    def test_insertUser(self):
        test_DB = DB.DataBase('test')
        phone = '7754000000'
        index = 1
        image =  'test'
        self.assertEqual( test_DB.insertUser(phone , index, image), [])

    def test_insertKeeper(self):
        test_DB = DB.DataBase('test')
        phone = '7754000000'
        password = 1
        self.assertEqual(test_DB.insertKeeper(phone , password), [])

    def test_insertFeedback(self):
        test_DB = DB.DataBase('test')
        issue_text = 'this sucks'
        type = 'camera issue'
        self.assertEqual( test_DB.insertFeedBack(type , issue_text), [])

    def test_remove_record_keeper(self):
        test_DB = DB.DataBase('test')
        #inserting test keeper
        phone = '7754000000'
        password = 1
        test_DB.insertKeeper(phone , password)
        #[] for successful execution, None for failed
        self.assertEqual( test_DB.removeRecord(phone , 'keeper'), [])

    def test_remove_record_user(self):
        test_DB = DB.DataBase('test0')
        phone = '7754000000'
        index = 1
        image =  'test'
        test_DB.insertUser(phone , index, image)
        self.assertEqual( test_DB.removeRecord(phone , 'user'), [])

    def test_remove_record_feedback(self):
        test_DB = DB.DataBase('test1')
        issue_text = 'this sucks'
        type = 'camera issue'
        test_DB.insertFeedBack(type , issue_text)
        self.assertEqual( test_DB.removeRecord(issue_text , 'feedback'), [])

    

    def test_remove_issue(self):
        pass

    def test_getKeeperCount(self):
        test_DB = DB.DataBase('test')

    def test_retrieveKeeperUserPass(self):
        test_DB = DB.DataBase('test')

    def test_getUserAttempts(self):
        pass

    
        
        # functions to test for client
    '''
    def send_init_test(self):
    def check_for_master(self):
    def send_dep_key(self, phone, index, image):
    def get_keeper_passwords(self):
    def check_user_phone(self, phone):
    def check_keeper_phone(self, phone):
    def send_ret_key(self, image_array):
    def send_add_keeper(self, phone,  password):
    def send_feedback(self, type, issue_text):
    def arrayToHex(self, array):
    def file_to_hex(self, file_name):

    '''

     # functions to test for facial recognition
    '''
    def delete_entry(self, phone_key):
    def add_user_face_encoding(self, phone_key, encoding_val):
    def recognize_face(self, frame):
    def reset_recognized_face(self):
    '''


#integration testing server + db + face rec + client (can't really test server alone)
#issue testing server, it's not initiated in class, it's initiated when 
def clean_up():
        #delete test databases
        test_DB = DB.DataBase('test1')
        test_db_list = ['test', 'test0', 'test1']
        for i in test_db_list:
            test_DB.delete_db(i)

if __name__ == '__main__':
    #clean_up()#run after
    u.main()    
    
