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
from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import SpinnerOption
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

#wifi+servercheck function
import subprocess
import platform
import socket

#Database Imports
import DatabaseClass as DB

# importing modules from other directories
import os

from FaceDetection.face_detect import Face_Detect
from FaceRecognition.FaceRec import Face_Recognition
from ServerClient.client import SendData

# global variables with initialization
global photoFlag 
photoFlag = False
global full_name
full_name = ""

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

class CustomDropDown(DropDown):
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
        def on_pre_enter(self, *args):
                self.ids.bound.start_cam()
        def on_leave(self, *args):
                self.ids.bound.end_cam()
                #print(self.parent.ids)

class FaceRecognitionScreen(Screen):
        def on_pre_enter(self, *args):
                self.ids['cam'].start_cam()
        def on_leave(self, *args):
                self.ids['cam'].end_cam()

#class MySpinnerOption(SpinnerOption):
#        pass

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

class BoundingPreview(Image):
        # variables
        convertedImage = None
        faces = None
        imageName = "image.jpeg" #default name

        def __init__(self, **kwargs):
                super(BoundingPreview, self).__init__(**kwargs)
                self.cascade = cv2.CascadeClassifier('FaceDetection/haarcascade_frontalface_default.xml')
                global photoFlag
                photoFlag = False
                
        def start_cam(self):
                self.video = cv2.VideoCapture(0)
                #set frame rate
                Clock.schedule_interval(self.update, 1.0 / 30)

        def end_cam(self):
                self.video.release()

        # uses the cascade to detect the faces within the given image
        def setFaces(self):
                self.faces = self.cascade.detectMultiScale(self.convertedImage, scaleFactor = 1.2, minNeighbors = 6, minSize = (30, 30), flags = None)
        
        # handles drawing the green rectangle around the detected faces
        # also crops and saves the image (should use a naming scheme in future for saving images)
        def drawRectangleImage(self):
                global full_name

                for (x,y,w,h) in self.faces:
                        cv2.rectangle(self.image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        self.image = self.image[y:y+h, x:x+w]
                if not full_name == "":
                        self.imageName = str(full_name) + ".jpeg"
                cv2.imwrite(self.imageName, self.image)
                
        # draws a green rectangle around the detected face
        def drawRectangleVideo(self):
                for (x,y,w,h) in self.faces:
                        cv2.rectangle(self.image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # called through a schedule to capture a single frame/image
        # calls other class functions to perform face detection
        def update(self, dt):
                ret, self.image = self.video.read()
                if self.video.isOpened():
                        self.convertedImage = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
                        self.setFaces()
                        self.drawRectangleVideo()
                        #Convert to Kivy Texture
                        buf = cv2.flip(self.image, 0).tobytes()
                        texture = Texture.create(size=(self.image.shape[1], self.image.shape[0]), colorfmt='bgr') 
                        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                        #Change the texture of the instance
                        self.texture = texture
                        if(photoFlag == True):
                                self.drawRectangleImage()


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
                
                '''These are for testing and can be removed once GUI exists for them'''
                self.check_wifi()
                self.check_server()
                
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
                if platform.system() != "Windows":
                        try:
                                output = subprocess.check_output(['sudo', 'iwgetid'])
                                #output = output.split('"')[1]
                                
                                for line in output.split():
                                        line = line.decode("utf-8")
                                        if line[:5]  == "ESSID":
                                                ssid = line.split('"')[1]
                                print('\x1b[6;30;42m' + 'Connected Wifi SSID: ' + ssid + '\x1b[0m')
                                #print("Connected Wifi SSID: " + output.split('"')[1])
                                return True
                        except Exception as e:
                                print('\x1b[6;30;41m' + e + 'no wifi'+ '\x1b[0m')
                                #print (e, "no wifi")
                                return False
                else: 
                        print('\x1b[6;30;42m' + 'Platform is Windows, Skipping WiFi Checks, returning True'+ '\x1b[0m')
                        return True
        
        ''' THIS FUNCTION WILL CHECK THAT OFFSITE SERVER IS RESPONDING '''
        def check_server(self):
                test = SendData()
                
                try:
                        if test.send_init_test() is True:
                                print('\x1b[6;30;42m' + 'Server is Online and Responding'+ '\x1b[0m')
                                return True
                        else:
                                print('\x1b[6;30;41m' + 'Server is not Responding'+ '\x1b[0m')
                                
                                print("Server is not Responding")
                                return False
                except Exception as e:
                        print('\x1b[6;30;41m' + 'Server is not Responding - Timeout'+ '\x1b[0m')

        
        ''' 
        
        THIS FUNCTION WILL CHECK IF MAIN KEEPER EXISTS IN DB (password plus username)
        
        BTW, DAWIT, CHECK_SERVER ABOVE MAY BE ABLE TO BE MODIFIED TO DO THAT ALREADY IN ONE REQUEST AND GET DB ENTRY, CONSIDER IT.
        
        '''
        def check_main_keeper_exists(self):
                pass

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
                           
                           WHEN PROGRAM FIRST RUNS NEED TO CHECK FOR WIFI, SERVER RESPONDING, AND DATABASE EXISTING ALREADY
                           
                           
                        '''  
                        
                            
                        '''
                        example:
                        client.send_dep_key(int(user id), str(full name), str (phonetext), int (key index), str (imagename) 
                        
                        if response = good, user added to db
                        if response = bad, user rejected, do not open inboxicated for deposit. Throw a message.
                        
                        '''
                                                                                                                             
                        
                        #self.root.ids.deposit.ids.full_name.text = ""		
                        #self.root.ids.deposit.ids.phone.text = ""
                        # here call face detection (work in progress)
                        self.set_name()
                        self.root.ids.deposit.switchScreen()
                        i_db.insertUser(new_id ,self.root.ids.deposit.ids.full_name.text, self.root.ids.deposit.ids.phone.text, 1, '')
                        # key indexing has not been implemented yet    

        def clear_deposit_info(self):		
                self.root.ids.deposit.ids.full_name.text = ""		
                self.root.ids.deposit.ids.phone.text = ""
                self.root.ids.deposit.ids.deposit_label.text = "Deposit Keys"

        def close_deposit_error(self, instance):
                self.deposit_message.dismiss()

        def take_photo(self):
                global photoFlag
                photoFlag = True

        def set_name(self):
                global full_name
                full_name = self.root.ids.deposit.ids.full_name.text

        def reset_name(self):
                global full_name
                full_name = ""
        
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
