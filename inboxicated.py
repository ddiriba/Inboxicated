# kivy imports
from ast import Pass
import kivy
import kivymd
from kivy.config import Config
from kivy.uix.vkeyboard import VKeyboard 
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480') 
Config.set('graphics', 'window_state', 'maximized')
Config.set('graphics', 'fullscreen', '1')
Config.set('kivy', 'keyboard_mode', 'systemandmulti')
Config.set('kivy', 'keyboard_layout', 'numeric.json')
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivymd.app import MDApp 
from kivymd.uix.card import MDCard
from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import SpinnerOption
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.uix.vkeyboard import VKeyboard
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.graphics.texture import Texture
from kivy.properties import StringProperty
kivy.require('2.0.0')

# registering our new custom fontstyle
from kivy.core.text import LabelBase
LabelBase.register(name='Bang', fn_regular='Bangers-Regular.ttf')

# other imports
from datetime import datetime
import random
import cv2
import threading 

#wifi+servercheck function
import subprocess
import platform
import socket

# importing modules from other directories
import os

#from FaceDetection.face_detect import Face_Detect
#from FaceRecognition.FaceRec import Face_Recognition
from ServerClient.client import SendData
# global variables with initialization
global photoFlag 
photoFlag = False
global full_name
full_name = ""
global phone_number
phone_number = ""

#Thermal Camera
#from Thermal.thermal import SeekPro

# import Raspberry Pi stuff
#from MotorControl.ServoControl import Servo
#from MotorControl.BoxController import Stepper


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

class RecognizerPopUp(Popup):
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

class FallBackScreen(Screen):
        def on_pre_enter(self):
                Inboxicated.get_running_app().doMath()
        pass

class OverrideScreen(Screen):
        pass

class DrunkDetectionScreen(Screen):
        pass
        '''
        def on_pre_enter(self, *args):
                self.ids[].start_cam()
        '''

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
                #try catch to ensure that if the camera is not accessible, there will be no attempts to access images
                try:
                        self.capture = cv2.VideoCapture(0)
                        assert self.capture.isOpened(), "Camera could not be accessed"
                except AssertionError as msg:
                        print(msg)
                #Set drawing interval
                Clock.schedule_interval(self.update, 1.0 / 30)
        '''
        Function called on leave from face recognition screen
        '''
        def end_cam(self):
                self.capture.release()
                cv2.destroyAllWindows()

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

"""   NEED TO WORK ON CREATING A CAMERA PREVIEW WITHIN AN APPP
class ThermalCameraPreview(Image):
        def __init__(self, **kwargs):
                super(ThermalCameraPreview, self).__init__(**kwargs)
        '''
        Function called on pre enter to face recognition screen
        '''
        def start_cam(self):
                #Connect camera
                #self.capture = SeekPro()
                #try catch to ensure that if the camera is not accessible, there will be no attempts to access images
                try:
                        self.capture = SeekPro()
                        assert self.capture.isOpened(), "Camera could not be accessed"
                except AssertionError as msg:
                        print(msg)
                #Set drawing interval
                Clock.schedule_interval(self.update, 1.0 / 30)
        '''
        Function called on leave from face recognition screen
        '''
        def end_cam(self):
                self.capture.release()
                cv2.destroyAllWindows()

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
"""
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
                #try catch to ensure that if the camera is not accessible, there will be no attempts to access images
                try:
                        self.video = cv2.VideoCapture(0)
                        assert self.video.isOpened(), "Camera could not be accessed"
                except AssertionError as msg:
                        print(msg)
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
                global phone_number

                for (x,y,w,h) in self.faces:
                        cv2.rectangle(self.image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        self.image = self.image[y:y+h, x:x+w]
                if not phone_number == "":
                        #self.imageName = "ServerClient//" + str(phone_number) + ".jpeg"
                        print('phone number wonky')
                        self.imageName = "ServerClient//" + str(phone_number) + ".jpeg"
                cv2.imwrite(self.imageName, self.image)
                print('image saved')
                
        # draws a green rectangle around the detected face
        def drawRectangleVideo(self):
                for (x,y,w,h) in self.faces:
                        cv2.rectangle(self.image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # called through a schedule to capture a single frame/image
        # calls other class functions to perform face detection
        def update(self, dt):
                global phone_number
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
                        if(photoFlag == True and phone_number != ""):
                                self.drawRectangleImage()

class KeyPad(GridLayout):
        def __init__(self, *args, **kwargs):
                super(KeyPad, self).__init__(*args, **kwargs)
                self.cols = 3
                self.spacing = 10
                self.createButtons()

        def createButtons(self):
                _list = [1, 2, 3 ,4, 5, 6, 7, 8, 9, 0, "<=", "Enter"]
                for num in _list:
                        self.add_widget(Button(text=str(num), on_release=self.onBtnPress))

        def onBtnPress(self, btn):
                screen = Inboxicated.get_running_app().root.ids.fallback
                answer_text = screen.ids.answer

                if btn.text.isdigit():
                        answer_text.text += btn.text
                if btn.text == "<=" and answer_text.text != "":
                        answer_text.text = answer_text.text[:-1]
                if btn.text == "Enter" and answer_text.text != "":
                        Inboxicated.get_running_app().verifyAnswer()
                        Inboxicated.get_running_app().clear_fallback_info()

class Keyboard(VKeyboard):
        def __init__(self, **kwargs):
                super().__init__(**kwargs)
        def on_touch_up(self, touch):
                app = Inboxicated.get_running_app()
                print("here")
                if  not self.collide_point(*touch.pos) and not app.root.text_input.collide_point(*touch.pos):
                        print("Touched outside the keyboard")

class Inboxicated(MDApp):
        def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.enter = None
                self.deposit_message = None
                self.assign_message = None
                self.add_message = None
                self.success_message = None
                self.report = None
                self.recognized_message = None
                self.face_name = None
                self.popup = None
                self.override_message = None
                self.client = SendData()
                '''These are for testing and can be removed once GUI exists for them'''
                self.check_wifi()
                self.check_server()
                #self.box_operator = Stepper()

                
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

        def add_numpad(self):
                keyboard = Keyboard()
                keyboard.layout = 'numeric.json'

                #keyboard = Window.request_keyboard()
      
        '''THIS FUNCTION WILL CHECK FOR WIFI CONNECTION'''
        def check_wifi(self):
                if platform.system() != "Windows":
                        try:
                                output = subprocess.check_output(['sudo', 'iwgetid'])
                                for line in output.split():
                                        line = line.decode("utf-8")
                                        if line[:5]  == "ESSID":
                                                ssid = line.split('"')[1]
                                print('\x1b[6;30;42m' + 'Connected Wifi SSID: ' + ssid + '\x1b[0m')
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
                try:
                        if self.client.send_init_test() == True:
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
            master_check = self.client.check_for_master()

            if master_check == 0:
                print('there are no keepers')
            elif master_check == 'Server Issue':
                print('there is a server issue')
            else:
                print('good to go')

        '''
        1. Functions related to Deposit Keys Screen
        '''
        def enter_info(self):  
                #deposit_response = self.client.send_dep_key(self) #success/phone already exists / box full / server issue
                deposit_checks = self.client.check_user_phone(self.root.ids.deposit.ids.user_phone.text)
                if not (self.root.ids.deposit.ids.user_phone.text).isnumeric() or (len(self.root.ids.deposit.ids.user_phone.text) != 10):                     
                        if not self.deposit_message:
                                self.deposit_message = MDDialog(
                                        title="ERROR",
                                        text="Invalid Phone Number",
                                        buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_deposit_error)])
                        self.deposit_message.open()
                elif deposit_checks == "Phone already exists" : #Proceed/phone already exists / box full / server issue
                        if not self.deposit_message:
                                self.deposit_message = MDDialog(
                                        title="ERROR",
                                        text="This phone number already exists in database. Please go to Retrieve Keys if you want to retrieve the deposited keys.",
                                        buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_deposit_error)])
                        self.deposit_message.open()       
                elif deposit_checks == "Box full" : #Proceed/phone already exists / box full / server issue
                        if not self.deposit_message:
                                self.deposit_message = MDDialog(
                                        title="ERROR",
                                        text="All slots in the box have been taken, apologies for the inconvinience",
                                        buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_deposit_error)])
                        self.deposit_message.open() 
                elif deposit_checks == "Proceed":
                        self.set_phone_number()
                        #self.root.ids.deposit.ids.deposit_label.text = f'Thank You {self.root.ids.deposit.ids.full_name.text}!'
                        if not self.deposit_message:
                                self.deposit_message = MDDialog(
                                        title=f'Thank You!',
                                        text="You were successfully added as a user. Now we're going to take the picture of your face to ensure your keys safety.",
                                        buttons=[MDFlatButton(text="Proceed", text_color=self.theme_cls.primary_color,on_release=self.close_deposit_success)])
                        self.deposit_message.open() 
                        # send entry to client
                        new_id = random.randrange(1,5000, 1)   
                        '''
                        Note to Andrew, not sure where the image is being stored, client.deposit keys needs all info
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
                        # key indexing has not been implemented yet    

        def clear_deposit_info(self):			
                self.root.ids.deposit.ids.user_phone.text = ""
                self.root.ids.deposit.ids.deposit_label.text = "Deposit Keys"

        def close_deposit_error(self, instance):
                self.deposit_message.dismiss()
                self.deposit_message = None

        def close_deposit_success(self, instance):
                self.deposit_message.dismiss()
                self.deposit_message = None
                self.root.ids.deposit.switchScreen()                

        def take_photo(self):
                global photoFlag
                photoFlag = True                

        def delete_photo(self):
                filename = "ServerClient//" + phone_number + ".jpeg" #name should be changed to phone num
                if os.path.exists(filename):
                        print("path exists")
                        os.remove(filename)
                        return True
                return False

        def set_phone_number(self):
                global phone_number
                phone_number = self.root.ids.deposit.ids.user_phone.text
                return phone_number

        def reset_phone_number(self):
                global phone_number
                phone_number = ""

        def send_info(self):
                global phone_number
                imageName = "ServerClient//" + phone_number + ".jpeg" #name should be changed to phone num
                #imageName =  str(phone_number) + ".jpeg" #name should be changed to phone num
                print(imageName)
                imageName = self.client.file_to_hex(imageName)
                self.client.send_dep_key(phone_number, 5, imageName)
                self.delete_photo()
                self.reset_phone_number()
        
        '''
        2. Functions related to "Retrieve Keys" Screen
        '''
        def recognize_face(self):
                print(type(self.root.ids.recognize.ids.cam.frame))
                success = self.client.send_ret_key(self.root.ids.recognize.ids.cam.frame) #success returns a phone number
                self.face_name = str(success)
                self.recognized_popup(self.face_name)
                
                '''
                NOTE TO DAWIT, ANDREW, JULIA, #success variable should be a phone number,
                we might need an if condition checking if we actually got a number,
                client, server, and db side have been implemented,
                note this has not been tested yet so let me know if things are funky,
                the retrieve index should return an integer form the db and that gets sent to the box operator class,
                opening the box needs to happen after drunk detection/fallback question happens
                '''
                #retrieved_index = self.client.send_ret_index(success)
                #self.box_operator.DeployIndex(retrieved_index)

        def recognized_popup(self, person_name):
                if not self.recognized_message:
                        if person_name.isnumeric():
                                self.recognized_message = MDDialog(
                                                title="Face Recognized",
                                                text="Recognized the owner of this phone number: {}.".format(person_name),
                                                buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_recognized_message_success)])
                        elif person_name == "Face Not Recognized":
                                self.recognized_message = MDDialog(
                                                title="Face Not Recognized",
                                                text="We did not recognize you as a user. Please try again or contact the keeper to receive help if you deposited your keys. Otherwise, stop messing up with 'retrieve keys' function. Our face recognition algorithm works :)".format(person_name),
                                                buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_recognized_message_error)])
                        elif person_name == "No Keys Deposited":
                                self.recognized_message = MDDialog(
                                                title="Face Not Recognized",
                                                text="No keys have been deposited. Please deposit keys first to access any of the compartments.".format(person_name),
                                                buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_recognized_message_error)])
                        elif person_name == "No Face In Image":
                                self.recognized_message = MDDialog(
                                                title="Face Not Recognized",
                                                text="We couldn't find a face in the image you provided. Please make sure your face is centered in the frame and the lighting is good when you take your picture again.",
                                                buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_recognized_message_try_again)])                                                 
                        self.recognized_message.open()
        def close_recognized_message_success(self, instance):
                self.recognized_message.dismiss()
                self.recognized_message = None
                self.root.current = 'drunk_det'

        def close_recognized_message_try_again(self, instance):
                self.recognized_message.dismiss()
                self.recognized_message = None
                self.root.current = 'recognize'

        def close_recognized_message_error(self, instance):
                self.recognized_message.dismiss()
                self.recognized_message = None
                self.root.current = 'main'

        def reset_message(self):
                self.recognized_message = None


        # variables for fallback
        constant = 0
        coefficient = 0
        variable = 0
        answer = 0
        questionString = StringProperty()
        def doMath(self):
                self.constant = random.randrange(1, 50)
                self.coefficient = random.randrange(1, 10)
                self.variable = random.randrange(0, 20)
                self.answer = self.constant + (self.coefficient * self.variable)
                self.questionString = (f"{self.coefficient}x + {self.constant} = {self.answer}")

        def verifyAnswer(self):
                if not self.deposit_message:
                                if float(self.root.ids.fallback.ids.answer.text) != self.variable:
                                        self.deposit_message = MDDialog(
                                                title="ERROR",
                                                text="Incorrect Answer",
                                                buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_deposit_error)])
                                        self.deposit_message.open()
                                elif float(self.root.ids.fallback.ids.answer.text) == self.variable:
                                        self.deposit_message = MDDialog(
                                                title="Sheesh You're So Smart",
                                                text="Correct Answer",
                                                buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_deposit_error)])
                                        self.deposit_message.open()
        
        def clear_fallback_info(self):
                self.root.ids.fallback.ids.answer.text = ""

        '''
        3. Functions related to "Assign New Keeper" Screen, including adding new keeper
        and checking the login information for main keeper
        '''
        def check_login(self):
                all_passwords = self.client.get_keeper_passwords() #needs to be tested
                print(all_passwords)
                keeper_phone = self.root.ids.assign.ids.keeper_phone.text
                keeper_access_code = self.root.ids.assign.ids.password.text
                if (not keeper_phone.isnumeric() or (len(keeper_phone) != 10)) and (not keeper_access_code.isnumeric() or len(keeper_access_code) != 6):
                        if not self.assign_message:
                                self.assign_message = MDDialog(
                                        title="ERROR",
                                        text="Invalid Phone Number and Access Code. Please make sure that the phone number and access code are correct.",
                                        buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_assign_error)])
                        self.assign_message.open()                          
                elif not keeper_phone.isnumeric() or (len(keeper_phone) != 10):
                        if not self.assign_message:
                                self.assign_message = MDDialog(
                                        title="ERROR",
                                        text="Invalid Phone Number. Please make sure the phone number you are providing is correct.",
                                        buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_assign_error)])
                        self.assign_message.open()       
                elif not keeper_access_code.isnumeric() or len(keeper_access_code) != 6:
                        if not self.assign_message:
                                self.assign_message = MDDialog(
                                        title="ERROR",
                                        text="Invalid Access Code. Please make sure the access code you are providing is correct. It should be a 6-digit number that you signed up with.",
                                        buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_assign_error)])
                        self.assign_message.open() 
                else:                 
                        #static passwords should be changed to pins
                        if self.root.ids.assign.ids.keeper_phone.text !='1122334455' and self.root.ids.assign.ids.password.text !='123456':
                                if not self.assign_message:
                                        self.assign_message = MDDialog(
                                                title="Incorrect phone or access code.",
                                                text="Try again.",
                                                buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_assign_error)])
                                self.assign_message.open()
                                self.root.ids.assign.ids.keeper_phone.text = ""		
                                self.root.ids.assign.ids.password.text = ""
                        else:
                                self.root.ids.assign.ids.keeper_phone.text = ""		
                                self.root.ids.assign.ids.password.text = ""
                                self.root.current = 'add'
                        
        def clear_assign_info(self):		
                self.root.ids.assign.ids.keeper_phone.text = ""		
                self.root.ids.assign.ids.password.text = ""

        def close_assign_error(self, instance):
                self.assign_message.dismiss()
                self.assign_message = None

        def add_keeper(self):
                keeper_phone = self.root.ids.add.ids.keeper_phone.text
                keeper_access_code = self.root.ids.add.ids.password.text
                keeper_phone_check = self.client.check_keeper_phone(keeper_phone)
                if (not keeper_phone.isnumeric() or (len(keeper_phone) != 10)) and (not keeper_access_code.isnumeric() or len(keeper_access_code) != 6):
                        if not self.add_message:
                                self.add_message = MDDialog(
                                        title="ERROR",
                                        text="Invalid Phone Number and Access Code. Please make sure that the phone number and access code are of correct length.",
                                        buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_add_phone_error)])
                        self.add_message.open()  
                elif not keeper_phone.isnumeric() or (len(keeper_phone) != 10):                     
                        if not self.add_message:
                                self.add_message = MDDialog(
                                        title="ERROR",
                                        text="Invalid Phone Number. Please make sure the phone number you are providing is correct.",
                                        buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_add_phone_error)])
                        self.add_message.open()
                elif not keeper_access_code.isnumeric() or len(keeper_access_code) != 6:
                        if not self.add_message:
                                self.add_message = MDDialog(
                                        title="ERROR",
                                        text="Invalid Access Code. Please make sure the access code you are providing is correct. It should be a 6-digit number that will be treated as login password.",
                                        buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_add_phone_error)])
                        self.add_message.open()
                else:
                        if keeper_phone_check == "Phone Already Exists":
                                if not self.add_message:
                                        self.add_message = MDDialog(
                                                title="Hi",
                                                text="It looks like you already are a keeper. No need to sign up again.",
                                                buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_add_keeper_error)])
                                self.add_message.open()   

                        else:
                                phone = self.root.ids.add.ids.keeper_phone.text
                                password = self.root.ids.add.ids.password.text
                                success = self.client.send_add_keeper(keeper_phone, password)
                                if success != "Server Issue":
                                        if not self.success_message:
                                                self.success_message = MDDialog(
                                                        title="Success",
                                                        text="You were successfully added to the list of the keepers. Users might contact you to receive help with the box malfunction.",
                                                        buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_success_message)])
                                        self.success_message.open()
                                #('generate random p_key for user' ,self.root.ids.deposit.ids.full_name.text, self.root.ids.deposit.ids.phone.text, 1, 'insert photo here' ) 
                
        def clear_add_info(self):		
                self.root.ids.add.ids.password.text = ""		
                self.root.ids.add.ids.keeper_phone.text = ""
        def close_add_phone_error(self, instance):
                self.add_message.dismiss()  
                self.root.ids.add.ids.keeper_phone.text = ""
                self.add_message = None
        def close_add_keeper_error(self, instance):
                self.add_message.dismiss()   
                self.add_message = None
                self.root.current = 'main'
                self.clear_add_info()
        def close_success_message(self, instance):
                self.success_message.dismiss()  
                self.success_message = None
                self.clear_add_info()
                self.root.current = 'main' 

        '''
        4. Functions related to "Summon the Keeper" Screen
        '''         
        def notify_the_keepers(self):
                pass

        '''
        5. Functions related to "Report a bug" Screen
        '''
        def send_report(self):
                report = self.root.ids.problem.ids.report.text 
                type = self.root.ids.problem.ids.spinner.text
                report_response = self.client.send_feedback(type, report)
                if not report:
                        self.report_message = MDDialog(
                                        title="ERROR",
                                        text="Report is empty. Please fill it in before submitting.",
                                        buttons=[MDFlatButton(text="Ok", text_color=self.theme_cls.primary_color,on_release=self.close_report_error)])
                        self.report_message.open()
                elif report_response == 'Server Issue':
                        self.report_message = MDDialog(
                                        title="ERROR",
                                        text="Server issue, please try again later.",
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

        '''
        Override opening functions
        '''
        def check_login_override(self):
                all_passwords = self.client.get_keeper_passwords() #needs to be tested
                print(all_passwords)
                keeper_phone = self.root.ids.override.ids.keeper_phone.text
                keeper_access_code = self.root.ids.override.ids.password.text
                if (not keeper_phone.isnumeric() or (len(keeper_phone) != 10)) and (not keeper_access_code.isnumeric() or len(keeper_access_code) != 6):
                        if not self.override_message:
                                self.override_message = MDDialog(
                                        title="ERROR",
                                        text="Invalid Phone Number and Access Code. Please make sure that the phone number and access code are correct.",
                                        buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_assign_error)])
                        self.override_message.open()                          
                elif not keeper_phone.isnumeric() or (len(keeper_phone) != 10):
                        if not self.override_message:
                                self.override_message = MDDialog(
                                        title="ERROR",
                                        text="Invalid Phone Number. Please make sure the phone number you are providing is correct.",
                                        buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_assign_error)])
                        self.override_message.open()       
                elif not keeper_access_code.isnumeric() or len(keeper_access_code) != 6:
                        if not self.override_message:
                                self.override_message = MDDialog(
                                        title="ERROR",
                                        text="Invalid Access Code. Please make sure the access code you are providing is correct. It should be a 6-digit number that you signed up with.",
                                        buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_assign_error)])
                        self.override_message.open() 
                else:                 
                        #static passwords should be changed to pins
                        if self.root.ids.override.ids.keeper_phone.text !='1122334455' and self.root.ids.override.ids.password.text !='123456':
                                if not self.override_message:
                                        self.override_message = MDDialog(
                                                title="Incorrect phone or access code.",
                                                text="Try again.",
                                                buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_assign_error)])
                                self.override_message.open()
                                self.root.ids.override.ids.keeper_phone.text = ""		
                                self.root.ids.override.ids.password.text = ""
                        else:
                                self.root.ids.override.ids.keeper_phone.text = ""		
                                self.root.ids.ovveride.ids.password.text = ""
                                #self.root.current = 'add' here add next screen 
                        
        def clear_override_info(self):		
                self.root.ids.override.ids.keeper_phone.text = ""		
                self.root.ids.override.ids.password.text = ""

        def close_override_error(self, instance):
                self.override_message.dismiss()
                self.override_message = None

if __name__ == "__main__":
        Inboxicated().run()
