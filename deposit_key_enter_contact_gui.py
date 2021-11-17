#pip install kivy[full]
from kivy.lang import Builder
#pip install kivymd
from kivymd.app import MDApp
from kivy.uix.vkeyboard import VKeyboard
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout


class LeftLabel(Label):
   def on_size(self, *args):
      self.text_size = self.size
      
    
class EnterContact(MDApp):
    def build(self):
        layout = GridLayout(cols=1)
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        self.topdisplay = Label(text="Depositing Keys", size_hint=(1, .1))
        self.instruction = Label(text="Enter Contact Information", size_hint = (1, .1))
        self.namelabel = LeftLabel(text="Name:", size_hint=(1,.1), halign = "left")
        self.phonlabel = LeftLabel(text="Phone Number:", size_hint=(1,.1), halign = "left")
        self.picksqlabel = LeftLabel(text="Pick Security Question:", size_hint=(1,.1), halign = "left")
        self.ansssqlabel = LeftLabel(text="Security Question Answer:", size_hint=(1,.1), halign = "left")
        self.button = Button(text="Submit", size_hint=(1,.1))
        keyboard = VKeyboard(on_key_up = self.key_up)
        
        layout.add_widget(self.topdisplay)
        layout.add_widget(self.instruction)
        layout.add_widget(self.namelabel)
        layout.add_widget(self.phonlabel)
        layout.add_widget(self.picksqlabel)
        layout.add_widget(self.ansssqlabel)
        layout.add_widget(self.button)
        layout.add_widget(keyboard)
        
        return layout
    
    def key_up(self, keybaord, keycode, *args):
        if isinstance(keycode, tuple):
            keycode = keycode[1]
            #hard part lol
        
EnterContact().run()
