'''
Code for utilizing TMC2209 Stepper Driver from https://github.com/Chr157i4n/TMC2209_Raspberry_Pi

Home motor Function, decide reverse, deploy index & main by John B.
'''

#from MotorControl.BC_old import Stepper
from MotorControl.TMC_2209.TMC_2209_StepperDriver import *
import time
import RPi.GPIO as GPIO

from MotorControl.ServoControl3 import *

import threading
import ctypes

class Stepper:
    def __init__(self):
        print("BoxController created.")
        
    def ran(self):
        print("In Run")

        '''
        Initialization of the stepper motor driver
        '''
        self.tmc = TMC_2209(16, 20, 21)
        self.tmc.setLoglevel(Loglevel.none)
        self.tmc.setMovementAbsRel(MovementAbsRel.absolute)
        self.tmc.setDirection_reg(False)
        self.tmc.setVSense(True)
        self.tmc.setCurrent(600)
        self.tmc.setIScaleAnalog(True)
        self.tmc.setInterpolation(True)
        self.tmc.setSpreadCycle(False)
        self.tmc.setMicrosteppingResolution(2)
        self.tmc.setInternalRSense(False)
        self.tmc.readIOIN()
        self.tmc.readCHOPCONF()
        self.tmc.readDRVSTATUS()
        self.tmc.readGCONF()
        self.tmc.setAcceleration(2000)
        self.tmc.setMaxSpeed(500)
        self.tmc.setMotorEnabled(True)
        
        
        self.aservo = MyServo()   
        sleep(0.5)
        #self.aservo.ActivateServo("close", 0)
        self.aservo.servo.value = 0.6
        sleep(1.5)
        
        self.HomeStepper()

        self.tmc.setMotorEnabled(False)
    
        time.sleep(1)
        try:
            del self.aservo
        except:
            print("Did not delete servo")
            pass
        try:
            del self.tmc
        except:
            print("Did not delete TMC")
            pass
        
        
    def HomeStepper(self):
        #print("---")
        print("Homing Motor")
        #print("---")

        #-----------------------------------------------------------------------
        # Home Motor
        #-----------------------------------------------------------------------

        GPIO.setmode(GPIO.BCM)
        GPIO_PIR = 4

        GPIO.setup(GPIO_PIR, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        
        while GPIO.input(GPIO_PIR) == GPIO.LOW:
            self.tmc.makeAStep()
            time.sleep(0.002)
            step = self.tmc.getCurrentPosition()
            step = step + 1
            self.tmc.setCurrentPosition(step)
        time.sleep(0.2)
        
        for x in range(200):
            self.tmc.makeAStep()
            time.sleep(0.004)
            
        step = self.tmc.getCurrentPosition()
        step = step + 1
        self.tmc.setCurrentPosition(step)
        
            
        self.tmc.setDirection_reg(1)

        while GPIO.input(GPIO_PIR) == GPIO.LOW:
            self.tmc.makeAStep()
            time.sleep(0.008)
        
        for x in range(35):
            self.tmc.makeAStep()
            time.sleep(0.008)
            
        time.sleep(0.2)    
        self.tmc.setCurrentPosition(0)


        self.tmc.setDirection_reg(0)

        self.tmc.setMotorEnabled(False)


        #print("---")
        print("Motor Homed")
        #print("---")
        
        return True

    def DeployIndex(self, index):
        print("In Deploy Index")
        
        '''
        Initialization of the stepper motor driver
        '''
        self.tmc = TMC_2209(16, 20, 21)
        self.tmc.setLoglevel(Loglevel.none)
        self.tmc.setMovementAbsRel(MovementAbsRel.absolute)
        self.tmc.setDirection_reg(False)
        self.tmc.setVSense(True)
        self.tmc.setCurrent(600)
        self.tmc.setIScaleAnalog(True)
        self.tmc.setInterpolation(True)
        self.tmc.setSpreadCycle(False)
        self.tmc.setMicrosteppingResolution(2)
        self.tmc.setInternalRSense(False)
        self.tmc.readIOIN()
        self.tmc.readCHOPCONF()
        self.tmc.readDRVSTATUS()
        self.tmc.readGCONF()
        self.tmc.setAcceleration(2000)
        self.tmc.setMaxSpeed(500)
        
        GPIO.setmode(GPIO.BCM)
        GPIO_PIR = 4

        GPIO.setup(GPIO_PIR, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        
        if index >= 0 and index <= 6:
            print("To Index = ", index)
            self.tmc.setMotorEnabled(True)
            self.sucessfulmove = self.DecideReverse(933 * index)
            print(self.tmc.getCurrentPosition())
            time.sleep(0.5)
            self.tmc.setMotorEnabled(False)
            
            if self.sucessfulmove == True:
                return True
            else:
                return False
            #return True
        else:
            print("Out of Range")
            return False

    
    
    def my_callback(self, channel):  
        print("StallGuard!")
        self.tmc.stop()

  
    def DecideReverse(self,step): 
        current = self.tmc.getCurrentPosition()
        #current index 4
        # 933 * 3
        
        #index 3?
        #absolute value of current - step
        #
        
        self.tmc.setStallguard_Callback(26, 1, self.my_callback) # after this function call, StallGuard is active #stallguard threshold is 1
            
        if current > step:
            print(current, step)
            self.tmc.setDirection_pin(0)
            finishedsuccessfully = self.tmc.runToPositionSteps(step)
        else:
            print(current, step)
            self.tmc.setDirection_pin(1)
            finishedsuccessfully = self.tmc.runToPositionSteps(step)
        
        GPIO.cleanup(26)
        if(finishedsuccessfully == True):
            print("Movement finished successfully")
            return True
        else:
            print("Motor Stalled!")  
            return False
        
           
    def OpenSlot(self):
        self.aservo = MyServo()
        print("OpenSlot - aservo created.")
        self.tmc.setMotorEnabled(True)
        self.aservo.ActivateServo("open", 0)
        time.sleep(5)
        print("OpenSlot - Deleting aservo")
        del self.aservo
        
        
        

    def CloseSlot(self):
        self.aservo = MyServo()
        print("CloseSlot - aservo created.")
        self.aservo.ActivateServo("close", 0)
        time.sleep(5)
        self.tmc.setMotorEnabled(False)
        print("CloseSlot - Deleting aservo")
        del self.aservo
        

if __name__ == "__main__":
    
    command = Stepper()
    command.DeployIndex(1)
    command.OpenSlot()
    command.CloseSlot()
    sleep(3)
    command = Stepper()
    command.DeployIndex(5)
    command.OpenSlot()
    command.CloseSlot()
    #del command.tmc
    #command.tmc.setMotorEnabled(False)
    