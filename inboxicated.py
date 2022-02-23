# kivy imports
import kivy
import kivymd
from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480') 
Config.set('kivy', 'keyboard_mode', 'systemandmulti')
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp 
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.graphics.texture import Texture
kivy.require('2.0.0')
# registering our new custom fontstyle
from kivy.core.text import LabelBase
LabelBase.register(name='Bang', fn_regular='Bangers-Regular.ttf')

# other imports
from datetime import datetime
import random
import cv2

#wifi function
import subprocess
import platform

#Database Imports
import DatabaseClass as DB

# importing modules from other directories
import os

from FaceDetection.face_detect import Face_Detect
from FaceRecognition.FaceRec import Face_Recognition

#Thermal Camera
#from Thermal.thermal import SeekPro

# import Raspberry Pi stuff
#from MotorControl.ServoControl import Servo
#from MotorControl.StepperControl import Stepper


class WelcomeScreen(Screen):
        def on_touch_move(self, touch):
                if touch.oy < touch.y:
                        Inboxicated.get_running_app().change_screen(screen_name="main", screen_direction="up")

class MainScreen(Screen):
        def on_touch_move(self, touch):
                if touch.y < touch.oy:
                        Inboxicated.get_running_app().change_screen(screen_name="welcome", screen_direction="down")

class DepositScreen(Screen):
        def switchScreen(self):
                Clock.schedule_once(self.callNext, 2)
        def callNext(self,dt):
                self.manager.current = 'loading'

class RetrieveScreen(Screen):
        pass

class SummonScreen(Screen):
        pass

class AssignScreen(Screen):
        pass

class WindowManager(ScreenManager):
        pass

class EnterContactInfo(MDCard):
        pass

class AddKeeperScreen(Screen):
        pass

class ReportProblemScreen(Screen):
        pass

class LoadingScreen(Screen):
        def on_enter(self): 
                label = kivymd.uix.label.MDLabel(halign= 'center', text= "Redirecting...", font_size= 50, pos_hint= {'center_x': 0.5, 'center_y': 0.5})
                self.add_widget(label)
                Clock.schedule_once(self.callNext, 2)
        def callNext(self,dt):
                self.manager.current = 'detect'
        
class FaceDetectionScreen(Screen):
        def on_enter(self, *args):
                faceDetect = Face_Detect('FaceDetection/haarcascade_frontalface_default.xml')
                faceDetect.detectVideo()
                #print(self.parent.ids)

class FaceRecognitionScreen(Screen):
        def on_pre_enter(self, *args):
                self.ids['cam'].start_cam()
        def on_leave(self, *args):
                self.ids['cam'].end_cam()

'''
Code for Camera Preview from https://linuxtut.com/en/a98280da7e6ba8d8e155/

'''
class CameraPreview(Image):
        def __init__(self, **kwargs):
                super(CameraPreview, self).__init__(**kwargs)
        '''
        Function called on pre enter to face recognition screen
        '''
        def start_cam(self):
                #Connect camera
                #self.capture = SeekPro()
                self.capture = cv2.VideoCapture(0)
                #Set drawing interval
                Clock.schedule_interval(self.update, 1.0 / 30)
        '''
        Function called on leave from face recognition screen
        '''
        def end_cam(self):
                self.capture.release()

        '''
        Drawing method to execute at intervals        
        '''
        def update(self, dt):
                #Load frame
                ret, self.frame = self.capture.read()
                if self.capture.isOpened():
                        #Convert to Kivy Texture
                        buf = cv2.flip(self.frame, 0).tobytes()
                        texture = Texture.create(size=(self.frame.shape[1], self.frame.shape[0]), colorfmt='bgr') 
                        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                        #Change the texture of the instance
                        self.texture = texture

class SaveButton(Button):
        #Execute when the button is pressed
        def on_press(self):
                #cv2.namedWindow("Your Face")
                #cv2.imshow("Your Face", self.preview.frame)
                #print(os.getcwd())
                #print(os.getcwd() + "\FaceRecognition\current_faces")
                pass
                
                #cv2.imwrite()
                #cv2.waitKey(0)
                #cv2.destroyAllWindows()

class Inboxicated(MDApp):
        def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.check_wifi()
                self.enter = None
                self.deposit_message = None
                self.assign_message = None
                self.add_message = None
                self.success_message = None
                self.report = None
                self.recognized_message = None
        '''
        Function that builds an app from inb.kv file, 
        refer to that file to change the layout or manage transition between screens
        '''        
        def build(self):
                self.faceCascade = 'haarcascade_frontalface_default.xml'
                self.theme_cls.theme_style = "Light"
                self.theme_cls.primary_palette = "BlueGray"
                return Builder.load_file("inb.kv")
        '''
        Function to change screens, pass the name of the screen and transition type like left, right etc
        '''
        def change_screen(self, screen_name, screen_direction):
                screen_manager = self.root
                screen_manager.current = screen_name
                screen_manager.transition.direction = screen_direction

        '''
        Helper functions for Database Information (save, retrieve etc.)
        '''
        
        '''THIS FUNCTION WILL CHECK FOR WIFI CONNECTION'''
        def check_wifi(self):
                if platform.system() is not "Windows":
                        try:
                                output = subprocess.check_output(['sudo', 'iwgetid'])
                                print("Connected Wifi SSID: " + output.split('"')[1])
                                return True
                        except Exception as e:
                                print (e, "no wifi")
                                return False
                else: 
                        print ("Platform is Windows, Skipping WiFi Checks, returning True")
                        return True
        
        ''' THIS FUNCTION WILL CHECK THAT OFFSITE SERVER IS RESPONDING '''
        def check_server(self):
                pass
        
        ''' THIS FUNCTION WILL CHECK IF MAIN KEEPER EXISTS IN DB (password plus username)'''
        def check_main_keeper_exists(self):
                pass
        
        ''' THIS FUNCTION WILL CHECK THAT OFFSITE SERVER IS RESPONDING '''

        '''
        1. Functions related to Deposit Keys Screen
        '''
        def enter_info(self):  
                if not (self.root.ids.deposit.ids.phone.text).isnumeric() or (len(self.root.ids.deposit.ids.phone.text) != 10):                     
                        if not self.deposit_message:
                                self.deposit_message = MDDialog(
                                        title="ERROR",
                                        text="Invalid Phone Number",
                                        buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_deposit_error)])
                        self.deposit_message.open()
                else:
                        self.root.ids.deposit.ids.deposit_label.text = f'Thank You {self.root.ids.deposit.ids.full_name.text}!'
                        # save entry to the database
                        new_id = random.randrange(1,5000, 1)
                        '''WE NEED FUNCTION HERE TO CHECK IF PHONE NUMBER EXISTS ALREADY (name-phone# key-value pairs)
                           SAME FOR ALL KEEPERS (add_keeper) LINE 250-ISH (main keeper is a keeper so phone and name can be retrieved/stored here)
                           USERNAME AND PASSWORD FOR MAIN KEEPER (WILL BE ADDED WHEN PROGRAM FIRST RUNS ())
                           
                           WHEN PROGRAM FIRST RUNS NEED TO CHECK FOR WIFI, INTERNET, SERVER RESPONDING, AND DATABASE EXISTING ALREADY
                           
                           
                        '''  
                        
                            
                        '''
                        
                        client.send_dep_key(int(user id), str(full name), str (phonetext), int (key index), str (imagename) 
                        
                        if response = good, user added to db
                        if response = bad, user rejected, do not open inboxicated for deposit. Throw a message.
                        
                        '''
                                                                                                                             
                        i_db.insertUser(new_id ,self.root.ids.deposit.ids.full_name.text, self.root.ids.deposit.ids.phone.text, 1, 'insert photo here' )
                        #self.root.ids.deposit.ids.full_name.text = ""		
                        #self.root.ids.deposit.ids.phone.text = ""
                        # here call face detection (work in progress)
                        self.root.ids.deposit.switchScreen()
                        # key indexing has not been implemented yet    

        def clear_deposit_info(self):		
                self.root.ids.deposit.ids.full_name.text = ""		
                self.root.ids.deposit.ids.phone.text = ""
                self.root.ids.deposit.ids.deposit_label.text = "Deposit Keys"

        def close_deposit_error(self, instance):
                self.deposit_message.dismiss()

        '''
        2. Functions related to "Retrieve Keys" Screen
        '''


        def recognize_face(self):
                face_recognizer = Face_Recognition(os.getcwd() + "\FaceRecognition\current_faces", testing_face_rec=False)           
                face_name = face_recognizer.recognize_face(self.root.ids.recognize.ids.cam.frame)
                self.recognized_popup(face_name)

        def recognized_popup(self, person_name):
                if not self.recognized_message:
                        self.recognized_message = MDDialog(
                                                title="Recognized Face",
                                                text=person_name,
                                                buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_recognized_message)])
                        self.recognized_message.open()
        def close_recognized_message(self, instance):
                self.recognized_message.dismiss()

        '''
        3. Functions related to "Assign New Keeper" Screen, including adding new keeper
        and checking the login information for main keeper
        '''
        def check_login(self):
                if self.root.ids.assign.ids.user.text !='team17' and self.root.ids.assign.ids.password.text !='inboxicated':
                        if not self.assign_message:
                                self.assign_message = MDDialog(
                                        title="Incorrect username or password.",
                                        text="Try again.",
                                        buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_assign_error)])
                        self.assign_message.open()
                        self.root.ids.assign.ids.user.text = ""		
                        self.root.ids.assign.ids.password.text = ""
                else:
                        self.root.ids.assign.ids.user.text = ""		
                        self.root.ids.assign.ids.password.text = ""
                        self.root.current = 'add'
                        
        def clear_assign_info(self):		
                self.root.ids.assign.ids.user.text = ""		
                self.root.ids.assign.ids.password.text = ""

        def close_assign_error(self, instance):
                self.assign_message.dismiss()

        def add_keeper(self):
                if not (self.root.ids.add.ids.phone.text).isnumeric() or (len(self.root.ids.add.ids.phone.text) != 10):                     
                        if not self.add_message:
                                self.add_message = MDDialog(
                                        title="ERROR",
                                        text="Invalid Phone Number",
                                        buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_add_error)])
                        self.add_message.open()
                else:
                        name = self.root.ids.add.ids.full_name.text
                        phone = self.root.ids.add.ids.phone.text
                        if not self.success_message:
                                self.success_message = MDDialog(
                                        title="Success",
                                        text="You were successfully added to the list of the keepers {}.".format(name),
                                        buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_success_message)])
                        self.success_message.open()
                        ('generate random p_key for user' ,self.root.ids.deposit.ids.full_name.text, self.root.ids.deposit.ids.phone.text, 1, 'insert photo here' ) 
                        # save it to database here
                        # master keeper flag defaulted to 0 for now
                        random.seed(datetime.now())
                        new_id = random.randrange(1,5000, 1)  
                        i_db.insertKeeper( new_id , name, phone, 0, 'insert photo here')
                        self.root.ids.add.ids.full_name.text = ""		
                        self.root.ids.add.ids.phone.text = ""
                
        def clear_add_info(self):		
                self.root.ids.add.ids.full_name.text = ""		
                self.root.ids.add.ids.phone.text = ""

        def close_add_error(self, instance):
                self.add_message.dismiss()   
        def close_success_message(self, instance):
                self.success_message.dismiss()  
                self.root.current = 'main' 

        '''
        4. Functions related to "Summon the Keeper" Screen
        '''         


        '''
        3. Functions related to "Report a bug" Screen
        '''
        def send_report(self):
                self.report = self.root.ids.problem.ids.report.text # send this to database in 'else'
                if not self.report:
                        self.report_message = MDDialog(
                                        title="ERROR",
                                        text="Report is empty. Please fill it in before submitting.",
                                        buttons=[MDFlatButton(text="Ok", text_color=self.theme_cls.primary_color,on_release=self.close_report_error)])
                        self.report_message.open()
                else:
                        self.report_message = MDDialog(
                                        title="Success",
                                        text="Report was successfuly sent to developers.",
                                        buttons=[MDFlatButton(text="Ok", text_color=self.theme_cls.primary_color,on_release=self.close_report_error)])
                        self.report_message.open()
                        
        def close_report_error(self, instance):
                self.report_message.dismiss()
        def clean_report_box(self):
                self.root.ids.problem.ids.report.text = ""

if __name__ == "__main__":
        i_db = DB.DataBase('inboxicated') 
        Inboxicated().run()
