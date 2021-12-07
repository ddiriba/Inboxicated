from gpiozero import AngularServo
from time import sleep
#import random
#from random import seed

#this file contains the Servo class, send parameter "open" or "close"
servo = AngularServo(17, min_angle=0, max_angle=270, min_pulse_width=0.0005, max_pulse_width=0.0025)

class Servo():

    def ActivateServo(self, status, speed):
        
        #future implementation of speed for iris shutter.
        #need to use for loops and iterate through angles on the servo with delay calculated.
        #speed should be input as 1-10
        speed = speed / 1000

        if status == "close":
            servo.angle = 250
        if status == "open":
            servo.angle = 80
    def run_demonstration(self):
        self.ActivateServo("open",10)
        sleep(5)
        self.ActivateServo("close",10)
        sleep(5)


#Testing Function, only run if script opened inside of ServoControl.py
if __name__ == "__main__":
    command = Servo()
    command.ActivateServo("open", 10)
    sleep(5)
    command.ActivateServo("close",10)
    sleep(5)
