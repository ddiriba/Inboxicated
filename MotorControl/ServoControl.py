from gpiozero import AngularServo
from time import sleep
#import random
#from random import seed

#this file contains the Servo class, send parameter "open" or "close"


class Servo():
    def __init__(self):
        print("Servo Constructor Called.")
        self.servo = AngularServo(17, min_angle=0, max_angle=270, min_pulse_width=0.0005, max_pulse_width=0.0025)
    
    def ActivateServo(self, status, speed):
        #speed should be an integer value, 0 results in highest possible speed of servo.
        #HIGHER NUMBERS RESULT IN LOWER SPEEDS DUE TO SLEEP CALCULATION IN FOR LOOP.
        
        try:
            speed = speed / 1000
        except:
            speed = 0
            pass

        if status == "close":
            for i in range(80,250,1):
                self.servo.angle = i
                sleep(speed)
            #servo.angle = 250
        if status == "open":
            for i in range(250,80,-1):
                self.servo.angle = i
                sleep(speed)
            #servo.angle = 80
    def run_demonstration(self):
        self.ActivateServo("open",10)
        sleep(5)
        self.ActivateServo("close",10)
        sleep(5)
        
    def __del__(self):
           self.servo.close()

#Testing Function, only run if script opened inside of ServoControl.py
if __name__ == "__main__":
    command = Servo()
    command.ActivateServo("open", 10)
    sleep(5)
    command.ActivateServo("close",10)
    sleep(5)
