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
import time

from picamera.array import PiRGBArray # Generates a 3D RGB array
from picamera import PiCamera # Provides a Python interface for the RPi Camera Module

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
        #self.web_cam = Image(size_hint=(1,.8), allow_stretch=True, keep_ratio=True)
        camera = PiCamera(framerate = 40)
        time.sleep(2)
        camera.resolution = (640,480)
        rawCapture = PiRGBArray(camera, size=camera.resolution)
        start = time.time()
        for frame, i in zip(camera.capture_continuous(rawCapture, format="bgr", use_video_port=True), range(400)):
            image = frame.array
            rawCapture.truncate(0)


        layout = BoxLayout(orientation = 'vertical')
        layout.add_widget(self.topdisplay)
        layout.add_widget(self.instruction)
        layout.add_widget(self.web_cam)
        layout.add_widget(self.button)
        layout.add_widget(self.verification)

        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH,640)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
        self.capture.set(cv2.CAP_PROP_FPS, 40)
        start = time.time()
        for i in range(400):
            ret, img = self.capture.read()

        

        Clock.schedule_interval(self.update, 1.0/33.0)

        return layout

    def update(self, *args):

        # Read frame from opencv
        ret, frame = self.capture.read()
        frame = frame#[120:120+250, 200:200+250, :]

        # Flip horizontal and convert image to texture
        buf = cv2.flip(frame, 0).tostring()
        img_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        img_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.web_cam.texture = img_texture


if __name__ == '__main__':
    CamApp().run()
