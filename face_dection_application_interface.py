# Application interface dependencies
#pip install kivy[full]
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
# Import kivy UX components
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics.texture import Texture

# Face detection dependencies
#pip install opencv-python
import cv2

#File storage 
#pip install os
import os #navigate through

#Resizing images/arrays
#pip install numpy
import numpy as np

# Build app and layout 
class CamApp(App):

    def build(self):
        self.topdisplay = Label(text="Retrieve Keys", size_hint=(1, .1))
        self.instruction = Label(text="Look at the Camera", size_hint = (1, .1))
        self.button = Button(text="Verify", size_hint=(1,.1))
        self.verification = Label(text="Verification Uninitated", size_hint=(1,.1))
        self.web_cam = Image(size_hint=(1,.8), allow_stretch=True, keep_ratio=True)
        

        layout = BoxLayout(orientation = 'vertical')
        layout.add_widget(self.topdisplay)
        layout.add_widget(self.instruction)
        layout.add_widget(self.web_cam)
        layout.add_widget(self.button)
        layout.add_widget(self.verification)

        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0/33.0)

        return layout

    def update(self, *args):

        # Read frame from opencv
        ret, frame = self.capture.read()
        frame = frame[120:120+250, 200:200+250, :]

        # Flip horizontal and convert image to texture
        buf = cv2.flip(frame, 0).tostring()
        img_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        img_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.web_cam.texture = img_texture


if __name__ == '__main__':
    CamApp().run()
