# kivy imports
from ast import Pass
import kivy
import kivymd
from kivy.config import Config
from kivy.uix.vkeyboard import VKeyboard
from matplotlib import scale 
#setting the kivy config parameters
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
from kivy.clock import Clock, mainthread
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.graphics.texture import Texture
from kivy.properties import StringProperty
kivy.require('2.0.0')

from functools import partial

import numpy as np
np.set_printoptions(threshold=np.inf)

# registering the font
from kivy.core.text import LabelBase
LabelBase.register(name='Bang', fn_regular='Bangers-Regular.ttf')

# other imports
from datetime import datetime
import random
import cv2
import threading 
import face_recognition
import traceback

#wifi+servercheck functionality
import subprocess
import platform
import socket

from functools import partial

# importing modules from other directories
import os
import examples.seek_renderer as ThermalCam
from ServerClient.client import SendData

# global variables with initialization
global photoFlag 
photoFlag = False
global full_name
full_name = ""
global phone_number
phone_number = ""
global countdown
countdown = 20

#Thermal Camera
from seekcamera import (
    SeekCameraIOType,
    SeekCameraColorPalette,
    SeekCameraManager,
    SeekCameraManagerEvent,
    SeekCameraFrameFormat,
    SeekCamera,
    SeekFrame,
)


# import Raspberry Pi modules
from MotorControl.ServoControl3 import MyServo
from MotorControl.BoxController import *

from MotorControl.TMC_2209.TMC_2209_StepperDriver import *




'''This class displays the welcome screen and also checks if there is a main keeper and if the server is up and running'''
class WelcomeScreen(Screen):
        def on_touch_move(self, touch):
                app = Inboxicated.get_running_app()
                if not Inboxicated.get_running_app().server_responding:
                        if not Inboxicated.get_running_app().server_message:
                                Inboxicated.get_running_app().server_message = MDDialog(
                                                title="Server is not responding",
                                                text="Close app and contact a designated keeper to resolve.",
                                                auto_dismiss=False,
                                                buttons=[MDFlatButton(text="Close App", text_color=Inboxicated.get_running_app().theme_cls.primary_color,on_release=Inboxicated.get_running_app().close_app)])
                        Inboxicated.get_running_app().server_message.open()                
                else:
                        if touch.oy < touch.y:
                                if app.check_main_keeper_exists() == 0:
                                        app.change_screen(screen_name="addmain", screen_direction="up")
                                else:
                                        app.change_screen(screen_name="main", screen_direction="up")
        #def on_enter(self, *args):

'''This class is has the logic for changing screens and also has the logic for the main screen'''
class MainScreen(Screen):
        def on_touch_move(self, touch):
                if touch.y < touch.oy:
                        Inboxicated.get_running_app().change_screen(screen_name="welcome", screen_direction="down")

'''This class displays the loading screen on deposit while the face recognition is being loaded'''
class DepositScreen(Screen):
        def switchScreen(self):
                Clock.schedule_once(self.callNext, 2)
        def callNext(self,dt):
                self.manager.current = 'loading'

'''kivy requires the following classes to be defined'''
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

class AddMainKeeperScreen(Screen):
        pass

class AddKeeperScreen(Screen):
        pass

class ReportProblemScreen(Screen):
        pass

'''Actual loading screen definition'''
class LoadingScreen(Screen):
        def on_enter(self): 
                label = kivymd.uix.label.MDLabel(halign= 'center', text= "Redirecting...", font_size= 50, pos_hint= {'center_x': 0.5, 'center_y': 0.5})
                self.add_widget(label)
                Clock.schedule_once(self.callNext, 2)
        def callNext(self,dt):
                self.manager.current = 'detect'

'''This class is for kivy and regards the face detection screen'''      
class FaceDetectionScreen(Screen):
        def on_pre_enter(self, *args):
                self.ids.bound.start_cam()
        def on_leave(self, *args):
                self.ids.bound.end_cam()
                 

'''This class is for kivy and regards the face recognition screen'''
class FaceRecognitionScreen(Screen):
        def on_pre_enter(self, *args):
                self.ids['cam'].start_cam()
        def on_leave(self, *args):
                self.ids['cam'].end_cam()

'''This class is for kivy and regards the fallback screen to do math problems'''
class FallBackScreen(Screen):
        def on_pre_enter(self):
                Inboxicated.get_running_app().doMath()
        pass

'''This class is for kivy and regards the override screen'''
class OverrideScreen(Screen):
        pass

'''this class is for kivy and regards the second part of the override process'''
class OverridePhoneScreen(Screen):
        pass

'''This class is for kivy and regards the display of the thermal camera preview'''
class DrunkDetectionScreen(Screen):
        
        def on_enter(self, *args):
                self.ids['thermal'].start_cam()
        
        '''def on_pre_enter(self, *args):
                if not self.ids['thermal'].start_cam():
                        app = Inboxicated.get_running_app()
                        app.thermal_not_working()'''

        def on_pre_leave(self, *args):
                self.ids['thermal'].end_cam()
        
class CloseBox(Screen):
        pass

class OpenBoxRetrieve(Screen):
        pass

class OpenBoxDeposit(Screen):
        pass

class OpenBoxOverride(Screen):
        pass

class BoxOpening(BoxLayout):
        pass

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

'''Contains camera and image data required to render images to the screen.'''
class Renderer:
        def __init__(self):
                self.busy = False
                self.frame = SeekFrame()
                self.camera = SeekCamera()
                 
                self.frame_condition = threading.Condition()
                self.first_frame = True
                 
        def __del__(self):
                self.frame_condition.acquire()
                self.frame_condition.release()
                print("RENDERER OBJECT DESTROYED")
                print('ACTIVE THREAD COUNT', threading.active_count())

                self.first_frame = False
                 


    
class ThermalCameraPreview(Image):
        def __init__(self, **kwargs):
                super(ThermalCameraPreview, self).__init__(**kwargs)                
                
        '''Thermal Rendering Functions'''
        def on_frame(self, _camera, camera_frame, renderer):
                """Async callback fired whenever a new frame is available.

                Parameters
                ----------
                _camera: SeekCamera
                        Reference to the camera for which the new frame is available.
                camera_frame: SeekCameraFrame
                        Reference to the class encapsulating the new frame (potentially
                        in multiple formats).
                renderer: Renderer
                        User defined data passed to the callback. This can be anything
                        but in this case it is a reference to the renderer object.
                """

                # Acquire the condition variable and notify the main thread
                # that a new frame is ready to render. This is required since
                # all rendering done by OpenCV needs to happen on the main thread.
                with renderer.frame_condition:
                        renderer.frame = camera_frame.color_argb8888
                        renderer.frame_condition.notify()


                '''Async callback fired whenever a camera event occurs.

                Parameters
                ----------
                camera: SeekCamera
                        Reference to the camera on which an event occurred.
                event_type: SeekCameraManagerEvent
                        Enumerated type indicating the type of event that occurred.
                event_status: Optional[SeekCameraError]
                        Optional exception type. It will be a non-None derived instance of
                        SeekCameraError if the event_type is SeekCameraManagerEvent.ERROR.
                renderer: Renderer
                        User defined data passed to the callback. This can be anything
                        but in this case it is a reference to the Renderer object.
                '''
        def on_event(self, camera, event_type, event_status, renderer):
                print(camera, event_type, event_status, renderer)
                
                print("{}: {}".format(str(event_type), camera.chipid))

                if event_type == SeekCameraManagerEvent.CONNECT:
                        print('actually connected on on_event')
                        if renderer.busy:
                                return

                        # Claim the renderer.
                        # This is required in case of multiple cameras.
                        renderer.busy = True
                        renderer.camera = camera

                        # Indicate the first frame has not come in yet.
                        # This is required to properly resize the rendering window.
                        renderer.first_frame = True

                        # Set a custom color palette.
                        # Other options can set in a similar fashion.
                        camera.color_palette = SeekCameraColorPalette.TYRIAN

                        # Start imaging and provide a custom callback to be called
                        # every time a new frame is received.
                        camera.register_frame_available_callback(self.on_frame, renderer)
                        camera.capture_session_start(SeekCameraFrameFormat.COLOR_ARGB8888)

                elif event_type == SeekCameraManagerEvent.DISCONNECT:
                        # Check that the camera disconnecting is one actually associated with
                        # the renderer. This is required in case of multiple cameras.
                        if renderer.camera == camera:
                                
                                # Stop imaging and reset all the renderer state.
                                camera.capture_session_stop()
                                #renderer.camera = None
                                renderer.frame = None
                                renderer.busy = False

                elif event_type == SeekCameraManagerEvent.ERROR:
                        print("{}: {}".format(str(event_status), camera.chipid))

                elif event_type == SeekCameraManagerEvent.READY_TO_PAIR:
                        return
                        
        '''
        Function called on pre enter to face recognition screen
        '''
        def start_cam(self):
                #Connect camera
                #try catch to ensure that if the camera is not accessible, there will be no attempts to access images
                try:    
                        self.manager = SeekCameraManager(SeekCameraIOType.USB)
                        # Start listening for events.
                        self.renderer = Renderer()
                        #Clock.schedule_once(self.my_callback, 1/5)
                        self.manager.register_event_callback(self.on_event, self.renderer)
 
                except AssertionError as msg:
                        print(msg)
                        return False
                
                #Set drawing interval
                Clock.schedule_interval(self.update, 1.0/30)

        '''
        Function called on leave from face recognition screen
        '''
        def end_cam(self):
                print("end_cam called")
                self.manager.destroy()

                #del self.renderer
                self.renderer.__del__()

        '''
        Drawing method to execute at intervals        
        '''
        def display_frame(self, frame):
                # display the current video frame in the kivy Image widget
                # create a Texture the correct size and format for the fra ume
                texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgra') 
                # copy the frame data into the texture
                texture.blit_buffer(frame.tobytes(order=None), colorfmt='bgra', bufferfmt='ubyte')
                # flip the texture (otherwise the video is upside down)
                #texture.flip_vertical()
                #texture.flip_horizontal()
                # actually put the texture in the kivy Image widget
                app = Inboxicated.get_running_app()
                app.root.ids.drunk_det.ids.thermal.texture = texture

        '''
        Update method for display_frame
        '''
        def update(self, dt):
                if self.renderer.first_frame == True:
                        with self.renderer.frame_condition:
                                if self.renderer.frame_condition.wait(200.0 / 1000.0):
                                        if not self.renderer.camera:
                                                print("destroyed camera")
                                        self.img = self.renderer.frame.data
                                        self.display_frame(self.img)
                else:
                        return False

        def my_callback(self, dt):
                pass            


''' 
Class for displaying face detection camera + face_detection bounding box.
'''
class BoundingPreview(Image):
        # variables
        convertedImage = None
        faces = None
        imageName = "image.jpeg" #default name
        noFace = False
        scale = 50

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
                self.faces = self.cascade.detectMultiScale(self.convertedImage, scaleFactor = 1.20, minNeighbors = 5, minSize = (30, 30), flags = None)
                if isinstance(self.faces, tuple):
                        self.noFace = True
                else:
                        self.noFace = False
        
        #handles drawing the green rectangle around the detected faces
        #also crops and saves the image (should use a naming scheme in future for saving images)
        def drawRectangleImage(self):
                global phone_number
                width = int(self.hiResImage.shape[1])
                height = int(self.hiResImage.shape[0])
                dim = (width, height)
                self.convertedImage = cv2.resize(self.convertedImage, dim, interpolation = cv2.INTER_AREA)
                self.setFaces()
                for (x,y,w,h) in self.faces:
                        area = (x+w) * (y + h)
                        if area > 28000:
                                cv2.rectangle(self.image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        self.image = self.image[y:y+h, x:x+w]
                if not phone_number == "":
                        print('phone number wonky')
                        self.imageName = "ServerClient//" + str(phone_number) + ".jpeg"
                cv2.imwrite(self.imageName, self.hiResImage)
                print('image saved')
                
        # draws a green rectangle around the detected face
        def drawRectangleVideo(self):
                for (x,y,w,h) in self.faces:
                        area = (x+w) * (y + h)
                        if area > 28000:
                                cv2.rectangle(self.image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                width = int(self.image.shape[1] * 100 / self.scale)
                height = int(self.image.shape[0] * 100 / self.scale)
                dim = (width, height)
                self.image = cv2.resize(self.image, dim, interpolation = cv2.INTER_AREA)

        # called through a schedule to capture a single frame/image
        # calls other class functions to perform face detection
        def update(self, dt):
                global phone_number
                global photoFlag
                ret, self.image = self.video.read()
                if self.video.isOpened():
                        self.hiResImage = self.image
                        width = int(self.image.shape[1] * self.scale / 100)
                        height = int(self.image.shape[0] * self.scale / 100)
                        dim = (width, height)
                        self.image = cv2.resize(self.image, dim, interpolation = cv2.INTER_AREA)
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
                                if self.noFace == True:
                                        print("nop face")
                                        Inboxicated.get_running_app().no_face()
                                else:
                                        print("Rectangle les go")
                                        self.drawRectangleImage()
                                photoFlag = False

'''
Class for displaying keyboard
'''
class Keyboard(VKeyboard):
        def __init__(self, **kwargs):
                super().__init__(**kwargs)
        def on_touch_up(self, touch):
                app = Inboxicated.get_running_app()
                print("here")
                if  not self.collide_point(*touch.pos) and not app.root.text_input.collide_point(*touch.pos):
                        print("Touched outside the keyboard")


'''
Main Inboxicated class
'''
class Inboxicated(MDApp):
        def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.enter = None
                self.deposit_message = None
                self.detected_message = None
                self.detected_success_message = None
                self.detected_failure_message = None
                self.assign_message = None
                self.add_message = None
                self.success_message = None
                self.report = None
                self.recognized_message = None
                self.face_name = None
                self.popup = None
                self.override_message = None
                self.thermal_message = None
                self.confirm_message = None
                self.password_check_message = None
                self.server_message = None
                self.no_face_error = False
                self.sober_message = None
                self.recognized_phone_number = None
                self.notify_message = None
                self.opening_index = None
                self.client = SendData()
                self.report_message = None

                '''These are for testing and can be removed once GUI exists for them'''
                self.check_wifi()
                ServoSuccess = False
                while ServoSuccess == False:
                        try:                
                                self.Initservo = MyServo()
                                print("INIT - Calling Close Servo")
                                self.Initservo.servo.value = 0.6
                                #del self.servo 
                        except:
                                print("INIT - Error in Servo, retrying...")
                                sleep(1)
                        else:
                                ServoSuccess = True

                self.server_responding = self.check_server()
                sleep(3)
                self.Initservo.servo.detach()
                del self.Initservo
        
        '''events to run when escape is pressed'''
        
        def on_stop(self):
                print('\x1b[6;30;42m' + 'Program Terminated Normally' + '\x1b[0m')
                #set servo Pulsewidth to 0
                self.servo_on_stop = MyServo()
                self.servo_on_stop.servo.value = 0.6
                sleep(3)
                self.servo_on_stop.servo.detach()
                print('\x1b[6;30;42m' + 'GPIO cleaned up - Servo Pulsewidth set to 0' + '\x1b[0m')                
               
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

        def close_app(self, instance):
                self.get_running_app().stop()

        def add_numpad(self):
                keyboard = Keyboard()
                keyboard.layout = 'numeric.json'

                #keyboard = Window.request_keyboard()
        
        def thermal_not_working(self):
                if not self.thermal_message:
                        self.thermal_message = MDDialog(
                                        auto_dismiss = False,
                                        title="Thermal Camera Cannot be Connected",
                                        text="Solve the Math Problem or Try Connecting to the Camera Again.\nHit 'Solve Math' to solve math equation or 'Try Again' to try reconnecting the Thermal Camera",
                                        buttons=[MDFlatButton(text="Solve Math", text_color=self.theme_cls.primary_color,on_release=self.switch_to_math), MDFlatButton(text="Try Again", text_color=self.theme_cls.primary_color,on_release=self.try_cam_again)])
                self.thermal_message.open()

        def switch_to_math(self, instance):
                self.thermal_message.dismiss()
                self.thermal_message = None
                self.change_screen('fallback', 'left')
        def try_cam_again(self, instance):
                self.thermal_message.dismiss()
                self.thermal_message = None
                self.change_screen('drunk_det', 'left')        

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
        '''

        def check_main_keeper_exists(self):
            master_check = self.client.check_for_master()

            if master_check == 0:
                print('There are no keepers')
                return 0
            elif master_check == 'Server Issue':
                print('There is a server issue')
            else:
                print('Server Responding, Main Keeper Present.')

        '''
        1. Functions related to Deposit Keys Screen
        '''
        def enter_info(self):  
                 
                #deposit_response = self.client.send_dep_key(self) #success/phone already exists / box full / server issue
                deposit_checks = self.client.check_user_phone(self.root.ids.deposit.ids.user_phone.text)
                if not (self.root.ids.deposit.ids.user_phone.text).isnumeric() or (len(self.root.ids.deposit.ids.user_phone.text) != 10):                     
                        if not self.deposit_message:
                                self.deposit_message = MDDialog(
                                        auto_dismiss = False,
                                        title="ERROR",
                                        text="Invalid Phone Number",
                                        buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_deposit_error)])
                        self.deposit_message.open()
                elif deposit_checks == "Phone Already Exists" : #Proceed/phone already exists / box full / server issue
                        if not self.deposit_message:
                                self.deposit_message = MDDialog(
                                        auto_dismiss = False,
                                        title="ERROR",
                                        text="This phone number already exists in database. Please go to Retrieve Keys if you want to retrieve the deposited keys.",
                                        buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_deposit_error)])
                        self.deposit_message.open()       
                elif deposit_checks == "Box full" : #Proceed/phone already exists / box full / server issue
                        if not self.deposit_message:
                                self.deposit_message = MDDialog(
                                        auto_dismiss = False,
                                        title="ERROR",
                                        text="All slots in the box have been taken, apologies for the inconvinience",
                                        buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_deposit_error)])
                        self.deposit_message.open() 
                elif deposit_checks == "Server Issue" : #Proceed/phone already exists / box full / server issue
                        if not self.deposit_message:
                                self.deposit_message = MDDialog(
                                        auto_dismiss = False,
                                        title="ERROR",
                                        text="Server supper dumb right now, try again later.",
                                        buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_deposit_error)])
                        self.deposit_message.open() 
                elif deposit_checks == "Server Down" : #Proceed/phone already exists / box full / server issue
                        if not self.deposit_message:
                                self.deposit_message = MDDialog(
                                        auto_dismiss = False,
                                        title="ERROR",
                                        text="Internet issues have risen, try agian later",
                                        buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_deposit_error)])
                        self.deposit_message.open() 
                elif deposit_checks >= "0" and deposit_checks <= "6":
                        
                        self.opening_index = int(deposit_checks)
                        self.set_phone_number()
                        #self.root.ids.deposit.ids.deposit_label.text = f'Thank You {self.root.ids.deposit.ids.full_name.text}!'
                        if not self.deposit_message:
                                self.deposit_message = MDDialog(
                                        auto_dismiss = False,
                                        title=f'Thank You!',
                                        text="You were successfully added as a user. Now we're going to take the picture of your face to ensure your keys safety.",
                                        buttons=[MDFlatButton(text="Proceed", text_color=self.theme_cls.primary_color,on_release=self.close_deposit_success)])
                        self.deposit_message.open()
                        #self.deposit_homeopen()
                        
                        # send entry to client
                        '''
                        Note to Andrew, not sure where the image is being stored, client.deposit keys needs all info
                        '''
                        '''
                        example:
                        client.send_dep_key(int(user id), str(full name), str (phonetext), int (key index), str (imagename) 
                        
                        if response = good, user added to db
                        if response = bad, user rejected, do not open inboxicated for deposit. Throw a message.
                        
                        '''

        
        '''the following function clears deposit info when the clear button is pressed'''
        
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

        '''delete photo after use'''

        def delete_photo(self):
                filename = "ServerClient//" + phone_number + ".jpeg" 
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

        def set_index_number(self, index_num):
                global index_number
                index_number = index_num
                return index_number

        def reset_index_number(self):
                global index_number
                index_number = ""
        
        '''
        Send info to server
        '''
        
        def send_info(self):
                global phone_number
                if not self.no_face_error and phone_number != None:
                        imageName = "ServerClient//" + phone_number + ".jpeg" 
                        print(imageName)
                        imageName = self.client.file_to_hex(imageName)
                        if imageName != 'Hex Conversion Error':
                                
                                server_response = self.client.send_dep_key(phone_number, self.opening_index, imageName)
                                #Successfull
                                #face not detected
                                if server_response == "Successful":
                                        pass
                                elif server_response == "Server down":
                                        print('server down')
                                        #go to main screen or server down pop up
                                elif server_response == "face not detected":
                                        print('face not detected')
                                        #go to face not detected screen/pop up
                                elif server_response == "Server Issue":
                                        print('server issue')
                                        #go to main screen or server down pop up
                                
                                #self.delete_photo()
                                #self.reset_phone_number()
                                self.reset_index_number()
                                if not self.detected_success_message:
                                        self.detected_success_message = MDDialog(
                                        auto_dismiss = False,
                                        title=f'Face Successfully Detected!',
                                        text="Your face has been successfully detected and stored.\nYou may now proceed to open the box and store your keys.",
                                        buttons=[MDFlatButton(text="Proceed", text_color=self.theme_cls.primary_color,on_release=self.go_to_open_box)])
                                self.detected_success_message.open() 
                else:
                        print("No info sent")
        
        '''change screen to open box screen'''
        
        def go_to_open_box(self, instance):
                self.change_screen(screen_name="open_deposit", screen_direction="left")
                self.detected_success_message.dismiss()
                self.detected_success_message = None

        '''
        No face detected popup.        
        '''
        def no_face(self):
                global photoFlag
                photoFlag = False
                self.no_face_error = True
                if not self.detected_message:
                        self.detected_message = MDDialog(
                                      auto_dismiss = False,
                                        title="Face Not Detected",
                                        text="Please make sure to face the camera directly forward.\nHit Try Again to take another photo.",
                                        buttons=[MDFlatButton(text="Try Again", text_color=self.theme_cls.primary_color,on_release=self.close_detected_message_try_again)])
                self.detected_message.open()

        
        def close_detected_message_try_again(self, instance):
                self.detected_message.dismiss()
                self.detected_message = None
                self.no_face_error = False
                self.root.current = 'detect'

        '''
        Prevention of returning to previous screen while phone being taken (photoFlag true)
        '''

        def photoTakingChangeScreen(self):
                global photoFlag
                if photoFlag is True:
                        print("Can't return after pressing take photo")
                        return
                else:
                        self.change_screen("main", "right")
        '''
        2. Functions related to "Retrieve Keys" Screen
        '''
        def recognize_face(self):
                 
                success = self.client.send_ret_key(self.root.ids.recognize.ids.cam.frame) #success returns a phone number
                self.face_name = str(success)
                self.recognized_popup(self.face_name)
                
                #retrieved_index = self.client.send_ret_index(success)
                #self.box_operator.DeployIndex(retrieved_index)

        '''
        Popup for when a face is recognized, also displays different error messages regarding this.
        '''
        def recognized_popup(self, person_name):
                if not self.recognized_message:
                        if person_name.isnumeric():
                                self.recognized_phone_number  = person_name
                                self.recognized_message = MDDialog(
                                        auto_dismiss = False,
                                                title="Face Recognized",
                                                text="Recognized the owner of this phone number: {}.".format(person_name),
                                                buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_recognized_message_success)])
                        elif person_name == "Face Not Recognized":
                                self.recognized_message = MDDialog(
                                        auto_dismiss = False,
                                                title="Face Not Recognized",
                                                text="We did not recognize you as a user. Please try again or contact the keeper to receive help if you deposited your keys. Otherwise, stop messing up with 'retrieve keys' function. Our face recognition algorithm works :)".format(person_name),
                                                buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_recognized_message_error)])
                        elif person_name == "No Keys Deposited":
                                self.recognized_message = MDDialog(
                                        auto_dismiss = False,
                                                title="No Keys Deposited",
                                                text="No keys have been deposited. Please deposit keys first to access any of the compartments.".format(person_name),
                                                buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_recognized_message_error)])
                        elif person_name == "No Face In Image":
                                self.recognized_message = MDDialog(
                                        auto_dismiss = False,
                                                title="No Face In Image",
                                                text="We couldn't find a face in the image you provided. Please make sure your face is centered in the frame and the lighting is good when you take your picture again.",
                                                buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_recognized_message_try_again)])                                                 
                        self.recognized_message.open()
        
        
        '''
        Functions for clearing data when leaving area or hitting clear button.
        '''
        def close_recognized_message_success(self, instance):
                self.recognized_message.dismiss()
                self.recognized_message = None
                # change this back later
                self.root.current = 'drunk_det'

        def close_recognized_message_try_again(self, instance):
                self.recognized_message.dismiss()
                self.recognized_message = None
                self.root.current = 'recognize'

        def close_recognized_message_error(self, instance):
                self.recognized_message.dismiss()
                self.recognized_message = None
                self.root.current = 'main'

        '''reset the recognized message when leaving'''
        
        def reset_message(self):
                self.recognized_message = None


        '''
        Function takes a photo of the user for the ML algorithm to process.
        '''
        
        def drunk_detect(self):
                thermal_photo = self.root.ids.drunk_det.ids.thermal.img
                print(thermal_photo.shape)
                cv2.imwrite('thermal.png', thermal_photo)
                Clock.schedule_once(self.deemed_sober, 5)


        '''
        Right now this function just says the feature is coming soon, later will allow a user to access keys.
        
        '''
        def deemed_sober(self, instance):
                print("")
                if not self.sober_message:
                        self.sober_message = MDDialog(
                                                auto_dismiss = False,
                                                title="This feature is coming soon.",
                                                text="Please solve the math equation instead.",
                                                buttons=[MDFlatButton(text="OK", text_color=self.theme_cls.primary_color,on_release=self.deemed_sober_go_to_open)])
                self.sober_message.open()
        
        
        def deemed_sober_go_to_open(self, instance):
                if self.sober_message:
                        self.sober_message.dismiss()
                self.sober_message = None  
                self.change_screen('fallback', 'left')

        # variables for fallback
        constant = 0
        coefficient = 0
        variable = 0
        answer = 0
        questionString = StringProperty()
        def doMath(self):
                self.constant = random.randrange(11, 99)
                self.coefficient = random.randrange(2, 15)
                self.variable = random.randrange(2, 20)
                self.answer = self.constant + (self.coefficient * self.variable)
                self.questionString = (f"{self.coefficient}x + {self.constant} = {self.answer}")

        def verifyAnswer(self):
                testAnswer = 193
                if not self.deposit_message:
                                if (self.root.ids.fallback.ids.answer.text == '') or (float(self.root.ids.fallback.ids.answer.text) != self.variable and float(self.root.ids.fallback.ids.answer.text) != testAnswer):
                                        self.deposit_message = MDDialog(
                                        auto_dismiss = False,
                                                title="ERROR",
                                                text="Incorrect Answer",
                                                buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.math_wrong_go_back)])
                                        #self.client.send_update_attempts(User_phoneNumber) -- function needs recognized number to be passed to this function
                                        self.deposit_message.open()
                                elif float(self.root.ids.fallback.ids.answer.text) == self.variable or float(self.root.ids.fallback.ids.answer.text) == testAnswer:
                                        self.deposit_message = MDDialog(
                                        auto_dismiss = False,
                                                title="Correct!",
                                                text="You will now be able to open the box.",
                                                buttons=[MDFlatButton(text="Proceed", text_color=self.theme_cls.primary_color,on_release=self.math_solved_open_box)])
                                        self.deposit_message.open()
        
        def clear_fallback_info(self):
                self.root.ids.fallback.ids.answer.text = ""

        def math_solved_open_box(self, instance):
                self.deposit_message.dismiss()
                self.deposit_message = None
                self.change_screen('open_retrieve', 'left')
                self.clear_fallback_info()

        def math_wrong_go_back(self, instance):
                self.client.send_update_attempts(self.recognized_phone_number)
                self.deposit_message.dismiss()
                self.deposit_message = None
                self.change_screen(screen_name='drunk_det', screen_direction='right')
                self.clear_fallback_info()

        def box_popup(self):
                 
                if not self.confirm_message:
                        self.confirm_message = MDDialog(
                                        auto_dismiss = False,
                                        title="Are you sure you want to go back?",
                                        text="If you click OK you will need to start the whole process of retrieving the keys over again.",
                                        buttons=[MDFlatButton(text="OK", text_color=self.theme_cls.primary_color,on_release=self.cancel_retrieving), MDFlatButton(text="CANCEL", text_color=self.theme_cls.primary_color,on_release=self.close_confirm_error)])
                self.confirm_message.open()          

        def close_confirm_error(self, instance):
                self.confirm_message.dismiss()
                self.confirm_message = None  
        def cancel_retrieving(self, instance):
                global phone_number
                self.client.send_ret_index(phone_number)
                self.reset_phone_number()
                self.confirm_message.dismiss()
                self.confirm_message = None 
                self.change_screen('main', 'right')        
        # called to deposit
        
        def deposit(self):
                self.reset_phone_number()
                param = 'deposit'
                popup = self.pop_up_box_opening()
                Clock.schedule_once(lambda dt: self.box_open_index(str(param)), 1) #this kinda works
                #Clock.schedule_once(lambda dt: , 1)
                Clock.schedule_once(self.go_to_close_box_screen, 2)
                
        def retrieve(self):
                param = 'retrieve'
                popup = self.pop_up_box_opening()
                Clock.schedule_once(lambda dt: self.box_open_index(str(param)), 1) # this kinda works
                Clock.schedule_once(self.go_to_close_box_screen, 2)                  

        def override_phone(self):
                #self.box_open_index('override')
                param = 'override'
                popup = self.pop_up_box_opening()
                Clock.schedule_once(lambda dt: self.box_open_index(str(param)), 1) # this kinda works
                Clock.schedule_once(self.go_to_close_box_screen, 2)  
                
        def bt_homeopen(self):
                index_retreive = self.client.send_ret_index(self.recognized_phone_number)
                print(index_retreive)
                self.deploy = Stepper()                
                polish_open_index = int(index_retreive)
                 
                self.deploy.DeployIndex(polish_open_index)
                
                #OpenSlot has a sleep of 5 in BoxController.py
                
                self.deploy.OpenSlot()
                self.dismiss_popup()

        def bt_close(self):
                self.deploy.CloseSlot()   
                     
                #Delete object to deinit.
                del self.deploy
                 
                self.change_screen('main', 'right')
        '''
        Function for box opening.
        '''              
        def box_open_index(self, param):
                index = None
                if param == 'retrieve':
                        index = self.client.send_ret_index(self.recognized_phone_number)
                elif param == 'deposit':
                        index = self.opening_index
                elif param == 'override':
                        index = self.phone_override
                self.deploy = Stepper()
                
                #homes stepper
                self.deploy.ran()
                print("Going to index: ", index)
                self.success = self.deploy.DeployIndex(index)
                
                if self.success == True:
                        print("Successful Deployment - Proceeding...")
                        self.deploy.OpenSlot()
                
                else:
                        print("Reached Failure State - Returning to Main Menu...")
                        #self.dismiss_popup()
                        
                        #self.detected_failure_message = MDDialog(auto_dismiss = False, title=f'ERROR: MOTOR FAILED TO HOME', text="PLEASE CONTACT KEEPER TO RESOLVE!", buttons=[MDFlatButton(text="Proceed", text_color=self.theme_cls.primary_color,on_release=self.change_screen('main', 'right'))])
                        self.change_screen('main', 'right')

                self.dismiss_popup()

        '''
        Function for box closing
        
        '''
        def box_close(self):
                
                print("in box_close")
                self.deploy.CloseSlot()

                del self.deploy
                
                self.change_screen('main', 'right')

        '''
        function for going to the close box screen
        '''
        
        def go_to_close_box_screen(self,instance):
                self.change_screen('close_box','left')

        
        '''
        Box opening popup screen and functions for closing it and a countdown (assuming threading this works correctly.)
        '''
        
        @mainthread
        def pop_up_box_opening(self):
                '''Displays a pop_up with a spinning wheel'''
                self.dialog = MDDialog(title="Opening the box...",auto_dismiss=False,type="custom",content_cls=BoxOpening())
                self.dialog.open()
        def dismiss_popup(self):
                self.dialog.dismiss() 
                self.dialog = None               
        def display_countdown(self, dt):
                global countdown
                countdown -= 1
                if countdown >= 0:
                        print(countdown)
                else:
                        return False
                
        '''
        3. Functions related to "Assign New Keeper" Screen, including adding new keeper
        and checking the login information for main keeper
        '''
        def check_login(self):
                all_passwords = self.client.get_keeper_passwords() #needs to be tested
                print(type(all_passwords))
                print(all_passwords)
                keeper_phone = self.root.ids.assign.ids.keeper_phone.text
                keeper_access_code = self.root.ids.assign.ids.password.text
                if (not keeper_phone.isnumeric() or (len(keeper_phone) != 10)) and (not keeper_access_code.isnumeric() or len(keeper_access_code) != 6):
                        if not self.assign_message:
                                self.assign_message = MDDialog(
                                        auto_dismiss = False,
                                        title="ERROR",
                                        text="Invalid Phone Number and Access Code. Please make sure that the phone number and access code are correct.",
                                        buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_assign_error)])
                        self.assign_message.open()                          
                elif not keeper_phone.isnumeric() or (len(keeper_phone) != 10):
                        if not self.assign_message:
                                self.assign_message = MDDialog(
                                        auto_dismiss = False,
                                        title="ERROR",
                                        text="Invalid Phone Number. Please make sure the phone number you are providing is correct.",
                                        buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_assign_error)])
                        self.assign_message.open()       
                elif not keeper_access_code.isnumeric() or len(keeper_access_code) != 6:
                        if not self.assign_message:
                                self.assign_message = MDDialog(
                                        auto_dismiss = False,
                                        title="ERROR",
                                        text="Invalid Access Code. Please make sure the access code you are providing is correct. It should be a 6-digit number that you signed up with.",
                                        buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_assign_error)])
                        self.assign_message.open() 
                else:                 
                        #static passwords should be changed to pins
                        if not (keeper_phone, keeper_access_code) in all_passwords.items():
                                if not self.assign_message:
                                        self.assign_message = MDDialog(
                                        auto_dismiss = False,
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
        
        '''
        Functions below are for clearing data when user hits clear button or leaves the area.
        '''
                      
        def clear_assign_info(self):		
                self.root.ids.assign.ids.keeper_phone.text = ""		
                self.root.ids.assign.ids.password.text = ""

        def close_assign_error(self, instance):
                self.assign_message.dismiss()
                self.assign_message = None

        '''
        Function for adding a keeper
        '''
        
        def add_keeper(self):
                keeper_phone = self.root.ids.add.ids.keeper_phone.text
                keeper_access_code = self.root.ids.add.ids.password.text
                keeper_access_code_check = self.root.ids.add.ids.password_check.text
                if keeper_access_code != keeper_access_code_check:
                        if not self.password_check_message:
                                self.password_check_message = MDDialog(
                                        title="Passwords don't match",
                                        text="Please make sure that the access codes match.",
                                        buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_pass_check)],
                                        auto_dismiss=False)
                        self.password_check_message.open()
                else:
                        keeper_phone_check = self.client.check_keeper_phone(keeper_phone)
                        if (not keeper_phone.isnumeric() or (len(keeper_phone) != 10)) and (not keeper_access_code.isnumeric() or len(keeper_access_code) != 6):
                                if not self.add_message:
                                        self.add_message = MDDialog(
                                        auto_dismiss = False,
                                                title="ERROR",
                                                text="Invalid Phone Number and Access Code. Please make sure that the phone number and access code are of correct length.",
                                                buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_add_phone_error)])
                                self.add_message.open()  
                        elif not keeper_phone.isnumeric() or (len(keeper_phone) != 10):                     
                                if not self.add_message:
                                        self.add_message = MDDialog(
                                        auto_dismiss = False,
                                                title="ERROR",
                                                text="Invalid Phone Number. Please make sure the phone number you are providing is correct.",
                                                buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_add_phone_error)])
                                self.add_message.open()
                        elif not keeper_access_code.isnumeric() or len(keeper_access_code) != 6:
                                if not self.add_message:
                                        self.add_message = MDDialog(
                                        auto_dismiss = False,
                                                title="ERROR",
                                                text="Invalid Access Code. Please make sure the access code you are providing is correct. It should be a 6-digit number that will be treated as login password.",
                                                buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_add_phone_error)])
                                self.add_message.open()
                        else:
                                if keeper_phone_check == "Phone Already Exists":
                                        if not self.add_message:
                                                self.add_message = MDDialog(
                                        auto_dismiss = False,
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
                                        auto_dismiss = False,
                                                                title="Success",
                                                                text="You were successfully added to the list of the keepers. Users might contact you to receive help with the box malfunction.",
                                                                buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_success_message)])
                                                self.success_message.open()
        
        
        '''
        Functions below are for clearing data when user leaves area either by choice, or pass/fail
        '''                                

        def close_pass_check(self, instance):
                self.password_check_message.dismiss()  
                self.root.ids.add.ids.password.text = ""
                self.root.ids.add.ids.password_check.text = ""
                self.password_check_message = None
             
        def clear_add_info(self):		
                self.root.ids.add.ids.password.text = ""
                self.root.ids.add.ids.password_check.text = ""		
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
        
        # functions for specifically adding a main keeper
        def add_main_keeper(self):
                keeper_phone = self.root.ids.addmain.ids.keeper_phone.text
                keeper_access_code = self.root.ids.addmain.ids.password.text
                keeper_access_code_check = self.root.ids.addmain.ids.password_check.text
                if keeper_access_code != keeper_access_code_check:
                        if not self.add_message:
                                self.add_message = MDDialog(
                                        title="Passwords don't match",
                                        text="Please make sure that the access codes match.",
                                        buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_add_main_phone_error)],
                                        auto_dismiss=False)
                        self.add_message.open()
                else:
                        if (not keeper_phone.isnumeric() or (len(keeper_phone) != 10)) and (not keeper_access_code.isnumeric() or len(keeper_access_code) != 6):
                                if not self.add_message:
                                        self.add_message = MDDialog(
                                                auto_dismiss = False,
                                                title="ERROR",
                                                text="Invalid Phone Number and Access Code. Please make sure that the phone number and access code are of correct length.",
                                                buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_add_main_phone_error)])
                                self.add_message.open()  
                        elif not keeper_phone.isnumeric() or (len(keeper_phone) != 10):                     
                                if not self.add_message:
                                        self.add_message = MDDialog(
                                                auto_dismiss = False,
                                                title="ERROR",
                                                text="Invalid Phone Number. Please make sure the phone number you are providing is correct.",
                                                buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_add_main_phone_error)])
                                self.add_message.open()
                        elif not keeper_access_code.isnumeric() or len(keeper_access_code) != 6:
                                if not self.add_message:
                                        self.add_message = MDDialog(
                                                auto_dismiss = False,
                                                title="ERROR",
                                                text="Invalid Access Code. Please make sure the access code you are providing is correct. It should be a 6-digit number that will be treated as login password.",
                                                buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_add_main_phone_error)])
                                self.add_message.open()
                        else:
                                phone = self.root.ids.addmain.ids.keeper_phone.text
                                password = self.root.ids.addmain.ids.password.text
                                success = self.client.send_add_keeper(keeper_phone, password)
                                if success != "Server Issue":
                                        if not self.success_message:
                                                self.success_message = MDDialog(
                                                auto_dismiss = False,
                                                        title="Success",
                                                        text="You were successfully added to the list of the keepers. Users might contact you to receive help with the box malfunction.",
                                                        buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_success_main_message)])
                                        self.success_message.open()
                
        '''
        Function for when a user clears the main message....clear message.
        '''
        
        def clear_add_main_info(self):		
                self.root.ids.addmain.ids.password.text = ""	
                self.root.ids.addmain.ids.password_check.text = ""
                self.root.ids.addmain.ids.keeper_phone.text = ""
       
        '''
        Function for when a user has an error and the main message needs to be closed....clear message.
        '''
        
        
        def close_add_main_phone_error(self, instance):
                self.add_message.dismiss()  
                self.root.ids.addmain.ids.keeper_phone.text = ""
                self.root.ids.addmain.ids.password_check.text = ""
                self.root.ids.addmain.ids.password.text = ""
                self.add_message = None
        
        '''
        Function for when a user has success and the main message needs to be closed....clear success message.
        '''
        
        def close_success_main_message(self, instance):
                self.success_message.dismiss()  
                self.success_message = None
                self.clear_add_main_info()
                self.root.current = 'main' 


        '''
        4. Functions related to "Summon the Keeper" Screen
        '''         
        def notify_the_keepers(self):
                check_success = self.client.send_notification()
                if check_success:
                        if not self.notify_message:
                                self.notify_message = MDDialog(
                                                auto_dismiss = False,
                                                title="Success",
                                                text="Keepers have been successfully notified.\nThe keeper(s) will arrive shortly.",
                                                buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_notify)])
                else:
                        if not self.notify_message:
                                self.notify_message = MDDialog(
                                                auto_dismiss = False,
                                                title="Something went wrong.",
                                                text="We're unable to notify the keepers right now.",
                                                buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_notify)])
                self.notify_message.open() 

        '''
        Functions for when leaving the notify screen...clear the message.
        '''
        
        def close_notify(self, instance):
                self.notify_message.dismiss()
                self.notify_message = None
                self.change_screen('main', 'right')
        '''
        5. Functions related to "Report a bug" Screen
        '''
        def send_report(self, feedback):
                sending_issue = feedback
                print(sending_issue)
                report_response = self.client.send_feedback(type, sending_issue)
                if not sending_issue:
                        if not self.report_message:
                                self.report_message = MDDialog(
                                                auto_dismiss = False,
                                                title="ERROR",
                                                text="Report is empty. Please fill it in before submitting.",
                                                buttons=[MDFlatButton(text="Ok", text_color=self.theme_cls.primary_color,on_release=self.close_report_error)])
                                self.report_message.open()
                elif report_response == 'Server Issue':
                        if not self.report_message:
                                self.report_message = MDDialog(
                                                auto_dismiss = False,
                                                title="ERROR",
                                                text="Server issue, please try again later.",
                                                buttons=[MDFlatButton(text="Ok", text_color=self.theme_cls.primary_color,on_release=self.close_report_error)])
                                self.report_message.open()
                else:
                        if not self.report_message:                        
                                self.report_message = MDDialog(
                                                auto_dismiss = False,
                                                title="Success",
                                                text="Report was successfuly sent to developers.",
                                                buttons=[MDFlatButton(text="Ok", text_color=self.theme_cls.primary_color,on_release=self.close_report_error)])
                                self.report_message.open()
        
        '''when leaving report error screen, clear the selected message'''
                   
        def close_report_error(self, instance):
                self.report_message.dismiss()
                self.report_message = None
                self.change_screen('main', 'right')


        '''
        Override opening functions and error message handling
        '''
        def check_login_override(self):
                all_passwords = self.client.get_keeper_passwords() #needs to be tested
                print(type(all_passwords))
                print(all_passwords)
                keeper_phone = self.root.ids.override.ids.keeper_phone.text
                keeper_access_code = self.root.ids.override.ids.password.text
                print(keeper_phone)
                print(keeper_access_code)
                if (not keeper_phone.isnumeric() or (len(keeper_phone) != 10)) and (not keeper_access_code.isnumeric() or len(keeper_access_code) != 6):
                        if not self.override_message:
                                self.override_message = MDDialog(
                                        auto_dismiss = False,
                                        title="ERROR",
                                        text="Invalid Phone Number and Access Code. Please make sure that the phone number and access code are correct.",
                                        buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_override_error)])
                        self.override_message.open()                          
                elif not keeper_phone.isnumeric() or (len(keeper_phone) != 10):
                        if not self.override_message:
                                self.override_message = MDDialog(
                                        auto_dismiss = False,
                                        title="ERROR",
                                        text="Invalid Phone Number. Please make sure the phone number you are providing is correct.",
                                        buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_override_error)])
                        self.override_message.open()       
                elif not keeper_access_code.isnumeric() or len(keeper_access_code) != 6:
                        if not self.override_message:
                                self.override_message = MDDialog(
                                        auto_dismiss = False,
                                        title="ERROR",
                                        text="Invalid Access Code. Please make sure the access code you are providing is correct. It should be a 6-digit number that you signed up with.",
                                        buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_override_error)])
                        self.override_message.open() 
                else:                 
                        #static passwords should be changed to pins
                        if not (keeper_phone, keeper_access_code) in all_passwords.items():
                                if not self.override_message:
                                        self.override_message = MDDialog(
                                        auto_dismiss = False,
                                                title="Incorrect phone or access code.",
                                                text="Try again.",
                                                buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_override_error)])
                                self.override_message.open()
                                self.root.ids.override.ids.keeper_phone.text = ""		
                                self.root.ids.override.ids.password.text = ""
                        else:
                                self.root.ids.override.ids.keeper_phone.text = ""		
                                self.root.ids.override.ids.password.text = ""
                                self.change_screen(screen_name="phone", screen_direction="left")
                                #self.root.current = 'add' here add next screen 
                        
        def clear_override_info(self):		
                self.root.ids.override.ids.keeper_phone.text = ""		
                self.root.ids.override.ids.password.text = ""

        def close_override_error(self, instance):
                self.override_message.dismiss()
                self.override_message = None

        def check_override_user_phone(self):
                phoneExists = self.client.send_ret_index(self.root.ids.phone.ids.user_phone.text)
                if(phoneExists == None or phoneExists == "Server Down" or phoneExists == "Server Issue"):
                        if not self.override_message:
                                self.override_message = MDDialog(
                                        auto_dismiss = False,
                                        title="ERROR",
                                        text="Invalid Phone Number.",
                                        buttons=[MDFlatButton(text="Close", text_color=self.theme_cls.primary_color,on_release=self.close_override_error)])
                        self.override_message.open()
                else:
                        self.phone_override = phoneExists
                        self.change_screen(screen_name= "open_override", screen_direction="left")
        

        def clear_override_user_phone_info(self):
                self.root.ids.phone.ids.user_phone.text = ""

        

if __name__ == "__main__":
        
        '''These are necessary to terminate pwm in case of crash or keyboard interrupt'''
        try:
                Inboxicated().run()
        except KeyboardInterrupt:
                print('\x1b[6;30;42m' + 'KeyboardInterrupt exception is caught' + '\x1b[0m')
                print("Active Threads ", threading.active_count())
                #clean up GPIO + set servo Pulsewidth to 0
                KBIServo = MyServo()
                KBIServo.servo.value = 0.6
                sleep(3)
                KBIServo.servo.detach()
                sleep(0.5)
                print('\x1b[6;30;42m' + 'GPIO cleaned up - Servo Pulsewidth set to 0' + '\x1b[0m')
        except Exception:
                #GPIO.cleanup()
                EXServo = MyServo()
                EXServo.servo.value = 0.6
                sleep(3)
                EXServo.servo.detach()
                sleep(0.5)
                print("Exception Called")
                print('\x1b[6;30;42m' + 'GPIO cleaned up - Servo Pulsewidth set to 0' + '\x1b[0m')
                print("Active Threads ", threading.active_count())
                traceback.print_exc()