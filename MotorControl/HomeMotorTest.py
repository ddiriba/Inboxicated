'''
Code for utilizing TMC2209 Stepper Driver from https://github.com/Chr157i4n/TMC2209_Raspberry_Pi

Home motor Function by John B.
'''

from TMC_2209.TMC_2209_StepperDriver import *
import time
import RPi.GPIO as GPIO

class Stepper:
        
    def __init__(self, name):
        
        homed = self.HomeStepper()
        
        
        
    def HomeStepper(self):
        print("---")
        print("Homing Motor")
        print("---")

        #-----------------------------------------------------------------------
        # initiate the TMC_2209 class
        # use your pins for pin_step, pin_dir, pin_en here
        #-----------------------------------------------------------------------
        tmc = TMC_2209(16, 20, 21)


        #-----------------------------------------------------------------------
        # set the loglevel of the libary (currently only printed)
        # set whether the movement should be relative or absolute
        # both optional
        #-----------------------------------------------------------------------
        tmc.setLoglevel(Loglevel.debug)
        tmc.setMovementAbsRel(MovementAbsRel.absolute)

        #-----------------------------------------------------------------------
        # these functions change settings in the TMC register
        #-----------------------------------------------------------------------
        tmc.setDirection_reg(False)
        tmc.setVSense(True)
        tmc.setCurrent(300)
        tmc.setIScaleAnalog(True)
        tmc.setInterpolation(True)
        tmc.setSpreadCycle(False)
        tmc.setMicrosteppingResolution(2)
        tmc.setInternalRSense(False)


        print("---\n---")

        #-----------------------------------------------------------------------
        # these functions read and print the current settings in the TMC register
        #-----------------------------------------------------------------------
        tmc.readIOIN()
        tmc.readCHOPCONF()
        tmc.readDRVSTATUS()
        tmc.readGCONF()

        print("---\n---")

        #-----------------------------------------------------------------------
        # set the Accerleration and maximal Speed
        #-----------------------------------------------------------------------
        tmc.setAcceleration(2000)
        tmc.setMaxSpeed(500)

        #-----------------------------------------------------------------------
        # activate the motor current output
        #-----------------------------------------------------------------------
        tmc.setMotorEnabled(True)

        #-----------------------------------------------------------------------
        # Home Motor
        #-----------------------------------------------------------------------

        GPIO.setmode(GPIO.BCM)
        GPIO_PIR = 4

        GPIO.setup(GPIO_PIR, GPIO.IN, pull_up_down = GPIO.PUD_UP)

        if GPIO_PIR == GPIO.HIGH:
            tmc.runToPositionSteps(10) 
        
        while GPIO.input(GPIO_PIR) == GPIO.LOW:
            tmc.makeAStep()
            time.sleep(0.002)

        time.sleep(0.2)   
        tmc.setDirection_reg(True)

        while GPIO.input(GPIO_PIR) == GPIO.LOW:
            tmc.makeAStep()
            time.sleep(0.008)
            print(tmc.getCurrentPosition())
            
            
        tmc.setCurrentPosition = 0


        tmc.setDirection_reg(False)

        #-----------------------------------------------------------------------
        # deactivate the motor current output
        #-----------------------------------------------------------------------
        tmc.setMotorEnabled(False)

        print("---\n---")

        #-----------------------------------------------------------------------
        # deinitiate the TMC_2209 class
        #-----------------------------------------------------------------------
        del tmc

        print("---")
        print("Motor Homed")
        print("---")
        return True

    def DeployIndex(self, index):
                #-----------------------------------------------------------------------
        # initiate the TMC_2209 class
        # use your pins for pin_step, pin_dir, pin_en here
        #-----------------------------------------------------------------------
        tmc = TMC_2209(16, 20, 21)


        #-----------------------------------------------------------------------
        # set the loglevel of the libary (currently only printed)
        # set whether the movement should be relative or absolute
        # both optional
        #-----------------------------------------------------------------------
        tmc.setLoglevel(Loglevel.debug)
        tmc.setMovementAbsRel(MovementAbsRel.absolute)

        #-----------------------------------------------------------------------
        # these functions change settings in the TMC register
        #-----------------------------------------------------------------------
        tmc.setDirection_reg(False)
        tmc.setVSense(True)
        tmc.setCurrent(300)
        tmc.setIScaleAnalog(True)
        tmc.setInterpolation(True)
        tmc.setSpreadCycle(False)
        tmc.setMicrosteppingResolution(2)
        tmc.setInternalRSense(False)


        print("---\n---")

        #-----------------------------------------------------------------------
        # these functions read and print the current settings in the TMC register
        #-----------------------------------------------------------------------
        tmc.readIOIN()
        tmc.readCHOPCONF()
        tmc.readDRVSTATUS()
        tmc.readGCONF()

        print("---\n---")

        #-----------------------------------------------------------------------
        # set the Accerleration and maximal Speed
        #-----------------------------------------------------------------------
        tmc.setAcceleration(2000)
        tmc.setMaxSpeed(500)

        #-----------------------------------------------------------------------
        # activate the motor current output
        #-----------------------------------------------------------------------

        #-----------------------------------------------------------------------
        # Move to Index
        #-----------------------------------------------------------------------
        if index == 0:
            return True
        elif index == 1:
            tmc.setMotorEnabled(True)
            return True

        elif index == 1:
            tmc.setMotorEnabled(True)
            return True
    
        elif index == 1:
            tmc.setMotorEnabled(True)
            return True
            
        elif index == 1:
            tmc.setMotorEnabled(True)
            return True
           
        elif index == 1:
            tmc.setMotorEnabled(True)
            return True
            
        elif index == 1:
            tmc.setMotorEnabled(True)
            return True
          
            
if __name__ == "__main__":
    command = Stepper()
    command.HomeStepper()
    time.sleep(5)
    command.DeployIndex(3)
    time.sleep(5)
            