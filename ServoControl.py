from gpiozero import AngularServo
from time import sleep
#import random
#from random import seed

#this file contains the Servo class, send parameter "open" or "close"
servo = AngularServo(17, min_angle=0, max_angle=270, min_pulse_width=0.0005, max_pulse_width=0.0025)

class Servo():
    def __init__(self, name):
        self.name = name

    def ActivateServo(self, status):
        if status == "close":
            servo.angle = 250
        if status == "open":
            servo.angle = 80


#TESTING BELOW THIS LINE
command = Servo('blankName')
command.ActivateServo("open")
sleep(5)
command.ActivateServo("close")
sleep(5)