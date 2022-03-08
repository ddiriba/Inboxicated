import unittest as u
import ServerClient.DatabaseClass as DB
import ServerClient.server as srvr
import ServerClient.client as clnt
import ServerClient.PictureFaceRecognition as pfr

#component testing
class TestDatabase(u.TestCase):
    def test_Hex_To_Array(self):
        test_DB = DB.DataBase()

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
    def insertKeeper(self,  Keeper_phone, Keeper_Password): 
    def insertFeedBack(self, IssueType, FeedBack):
    def removeRecord(self,  phone, user_type):
    def insertUser(self, user_phone, keyIndex, photo ): 
    def executeRecord(self, insert_query, data_tuple):

    '''
class TestDatabase(u.TestCase):
    def test_getUserCount(self):
        test_DB = DB.DataBase('test')

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

