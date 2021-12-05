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


class Inboxicated(MDApp):
        def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.enter = None
                self.deposit_message = None
        def build(self):
                self.theme_cls.theme_style = "Dark"
                self.theme_cls.primary_palette = "BlueGray"
                return Builder.load_file("inb.kv")

        def enter_info(self):  
                if not (self.root.ids.deposit.ids.phone.text).isnumeric():
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
                
        def clear_info(self):		
	        self.root.ids.deposit.ids.full_name.text = ""		
	        self.root.ids.deposit.ids.phone.text = ""
        def close_deposit_error(self, instance):
                self.deposit_message.dismiss()

if __name__ == "__main__":
        Inboxicated().run()