from adafruit_servokit import ServoKit
from time import sleep
import RPi.GPIO as GPIO

class Servo():
    def __init__(self):
        print("Servo Constructor Called.")
        self.servo = ServoKit(channels=16)
        self.servo.servo[0].actuation_range = 270
        
        #output enable pin (HIGH = OFF)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(24, GPIO.OUT)
        GPIO.output(24, GPIO.HIGH)
        
    def ActivateServo(self, status, speed):
        #speed should be an integer value, 0 results in highest possible speed of servo.
        #HIGHER NUMBERS RESULT IN LOWER SPEEDS DUE TO SLEEP CALCULATION IN FOR LOOP.
        
        try:
            speed = speed / 1000
        except:
            speed = 0
            pass

        if status == "close":
            GPIO.output(24, GPIO.LOW)
            self.servo.servo[0].angle = 270
            sleep(1)
            GPIO.output(24, GPIO.HIGH)
            #sleep(speed)
            #servo.angle = 250
        if status == "open":
            GPIO.output(24, GPIO.LOW)
            self.servo.servo[0].angle = 40
            sleep(1)
            GPIO.output(24, GPIO.HIGH)
            #sleep(speed)
            #servo.angle = 80
    def run_demonstration(self):
        self.ActivateServo("open",10)
        sleep(5)
        self.ActivateServo("close",10)
        sleep(5)
        
    def __del__(self):
        GPIO.cleanup(24)
        

#Testing Function, only run if script opened inside of ServoControl.py
if __name__ == "__main__":
    command = Servo()
    command.ActivateServo("open", 10)
    sleep(5)
    command.ActivateServo("close",10)
    sleep(5)
