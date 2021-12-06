import kivy
kivy.require('2.0.0')
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp 
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton


class MainScreen(Screen):
        pass

class DepositScreen(Screen):
        pass

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

class Inboxicated(MDApp):
        def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.enter = None
                self.deposit_message = None
                self.assign_message = None
                self.add_message = None
                self.success_message = None
        def build(self):
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
                        self.root.ids.deposit.ids.full_name.text = ""		
                        self.root.ids.deposit.ids.phone.text = ""
                        # here call face detection
                        # save entry to the database               
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
                        # save it to database here
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

if __name__ == "__main__":
        Inboxicated().run()