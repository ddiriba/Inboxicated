from gpiozero import Servo
from time import sleep

from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()
servo = Servo(24, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)

class Servo():
    def __init__(self):
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
            print("close servo")
            #for i in range(80,250,1):
            servo.value = 0.6
            #sleep(speed)
            #servo.angle = 250
        if status == "open":
            print("open servo")
            #for i in range(250,80,-1):
            servo.value = -0.75
            #sleep(speed)
            #servo.angle = 80
        sleep(1.5)
        servo.value = None
    def run_demonstration(self):
        self.ActivateServo("open",10)
        sleep(5)
        self.ActivateServo("close",10)
        sleep(5)
        
    def __del__(self):
        #THIS MUST BE CALLED TO TERMINATE PWM SIGNAL TO SERVO.
        print("Servo Destructor Called.")
        servo.value = None

#Testing Function, only run if script opened inside of ServoControl.py
if __name__ == "__main__":
    command = Servo()
    command.ActivateServo("open", 10)
    sleep(2)
    command.ActivateServo("close",10)
    sleep(2)
    #servo.value = -0.95
    #sleep(2)
    servo.value = None
    
    '''print("Start in the middle")
    servo.mid()
    sleep(5)
    print("Go to min")
    servo.min()
    sleep(5)
    print("Go to max")
    servo.max()
    sleep(5)
    print("And back to middle")
    servo.mid()
    sleep(5)
    servo.value = None'''
