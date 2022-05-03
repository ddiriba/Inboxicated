'''
Code for utilizing TMC2209 Stepper Driver from https://github.com/Chr157i4n/TMC2209_Raspberry_Pi

Home motor Function, decide reverse, deploy index & main by John B.
'''

from gpiozero import Servo
from time import sleep

from gpiozero.pins.pigpio import PiGPIOFactory

class MyServo():
    def __init__(self):
        self.factory = PiGPIOFactory()
        self.servo = Servo(18, initial_value=0.6, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=self.factory)
        print("Servo Constructor Called.")
        
    def ActivateServo(self, status, speed):
        #speed should be an integer value, 0 results in highest possible speed of servo.
        #HIGHER NUMBERS RESULT IN LOWER SPEEDS DUE TO SLEEP CALCULATION IN FOR LOOP.
        
        try:
            speed = speed / 1000
        except:
            speed = 0
            pass

        if status == "close":
            print("Servo Control Output - Close Servo")
            self.servo.value = 0.58
            sleep(1.5)
            #self.servo.detach()
            #sleep(0.5)
            
        if status == "open":
            print("Servo Control Output - Open Servo")
            self.servo.value = -0.72
            sleep(1.5)
            #self.servo.detach()
            #sleep(0.5)

    def end_servo_pwm(self):
        self.servo.detach()

    def __del__(self):
        #THIS MUST BE CALLED TO TERMINATE PWM SIGNAL TO SERVO.
        print("MyServo - OBJECT DELETED")
        try: 
            self.servo.detach()
        except:
            pass

#Testing Function, only run if script opened inside of ServoControl.py
if __name__ == "__main__":
    command = MyServo()
    command.ActivateServo("open", 10)
    sleep(2)
    command.ActivateServo("close",10)
    sleep(2)
    #servo.value = -0.95
    #sleep(2)
    command.servo.detach()

