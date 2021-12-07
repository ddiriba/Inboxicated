from gpiozero import AngularServo
from time import sleep
#import random
#from random import seed

#this file contains the Servo class, send parameter "open" or "close"
servo = AngularServo(17, min_angle=0, max_angle=270, min_pulse_width=0.0005, max_pulse_width=0.0025)

class Servo():
    def ActivateServo(self, status):
        if status == "close":
            servo.angle = 250
        if status == "open":
            servo.angle = 80
    def run_demonstration(self):
        self.ActivateServo("open")
        sleep(5)
        self.ActivateServo("close")
        sleep(5)

if __name__ == "__main__":
#TESTING BELOW THIS LINE COMMENT OUT TO USE IN OTHER FILES
    command = Servo()
    command.ActivateServo("open")
    sleep(5)
    command.ActivateServo("close")
    sleep(5)
