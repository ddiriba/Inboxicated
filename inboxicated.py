import kivy
import kivymd
import random
from datetime import datetime
import cv2
kivy.require('2.0.0')
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp 
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import DatabaseClass as DB
from kivy.clock import Clock
from kivy.graphics.texture import Texture


class MainScreen(Screen):
        pass

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
                self.capture = cv2.VideoCapture(0)
                Clock.schedule_interval(self.update, 1.0/33.0)
                #print(self.parent.ids)
        def update(self, *args):

                # Read frame from opencv
                ret, frame = self.capture.read()
                frame = frame[120:120+250, 200:200+250, :]

                # Flip horizontal and convert image to texture
                buf = cv2.flip(frame, 0).tostring()
                img_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                img_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                print(self.layout.ids.web_cam)
                self.web_cam.texture = img_texture


class Inboxicated(MDApp):
        def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.enter = None
                self.deposit_message = None
                self.assign_message = None
                self.add_message = None
                self.success_message = None
                self.report = None
        def build(self):
                self.faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
                self.theme_cls.theme_style = "Dark"
                self.theme_cls.primary_palette = "BlueGray"
                return Builder.load_file("inb.kv")

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
                        i_db.insertUser(new_id ,self.root.ids.deposit.ids.full_name.text, self.root.ids.deposit.ids.phone.text, 1, 'insert photo here' )
                        self.root.ids.deposit.ids.full_name.text = ""		
                        self.root.ids.deposit.ids.phone.text = ""
                        # here call face detection (work in progress)
                        self.root.ids.deposit.switchScreen()
                        # key indexing has not been implemented yet        
        def clear_deposit_info(self):		
	        self.root.ids.deposit.ids.full_name.text = ""		
	        self.root.ids.deposit.ids.phone.text = ""
        def close_deposit_error(self, instance):
                self.deposit_message.dismiss()

        def check_login(self):
                if self.root.ids.assign.ids.user.text!='team17' and self.root.ids.assign.ids.password.text !='inboxicated':
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
