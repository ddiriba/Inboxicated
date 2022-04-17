'''
Code for utilizing TMC2209 Stepper Driver from https://github.com/Chr157i4n/TMC2209_Raspberry_Pi

Home motor Function, decide reverse, deploy index & main by John B.
'''

from MotorControl.TMC_2209.TMC_2209_StepperDriver import *
import time
import RPi.GPIO as GPIO

from MotorControl.ServoControl3 import *

import threading
import ctypes

class thread_with_exception(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.run()
             
    def run(self):
        
        try:
            self.BoxControllerThread = Stepper()
            #while True:
            #    pass
        finally:
            pass
        # target function of the thread class
        '''try:
            while True:
                print('running ' + self.name)
        finally:
            print('ended')'''
          
    def get_id(self):
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id
  
    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
              ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception Raised - Thread Exiting')
        


class Stepper:
        
    def __init__(self):

        #close servo
        self.aservo = MyServo()   
        self.aservo.ActivateServo("close", 0)
        
        try:
            del self.aservo
        except:
            pass
        
        self.HomeStepper()
    
        time.sleep(1)
        try:
            del self.tmc
        except:
            pass
    def HomeStepper(self):
        #print("---")
        print("Homing Motor")
        #print("---")
        
                #-----------------------------------------------------------------------
        # initiate the TMC_2209 class
        # use your pins for pin_step, pin_dir, pin_en here
        #-----------------------------------------------------------------------
        self.tmc = TMC_2209(16, 20, 21)


        #-----------------------------------------------------------------------
        # set the loglevel of the libary (currently only printed)
        # set whether the movement should be relative or absolute
        # both optional
        #-----------------------------------------------------------------------
        self.tmc.setLoglevel(Loglevel.none)
        self.tmc.setMovementAbsRel(MovementAbsRel.absolute)

        #-----------------------------------------------------------------------
        # these functions change settings in the TMC register
        #-----------------------------------------------------------------------
        self.tmc.setDirection_reg(False)
        self.tmc.setVSense(True)
        self.tmc.setCurrent(600)
        self.tmc.setIScaleAnalog(True)
        self.tmc.setInterpolation(True)
        self.tmc.setSpreadCycle(False)
        self.tmc.setMicrosteppingResolution(2)
        self.tmc.setInternalRSense(False)


        #print("---\n---")

        #-----------------------------------------------------------------------
        # these functions read and print the current settings in the TMC register
        #-----------------------------------------------------------------------
        self.tmc.readIOIN()
        self.tmc.readCHOPCONF()
        self.tmc.readDRVSTATUS()
        self.tmc.readGCONF()

        #print("---\n---")

        #-----------------------------------------------------------------------
        # set the Accerleration and maximal Speed
        #-----------------------------------------------------------------------
        self.tmc.setAcceleration(2000)
        self.tmc.setMaxSpeed(500)

        #-----------------------------------------------------------------------
        # activate the motor current output
        #-----------------------------------------------------------------------
        self.tmc.setMotorEnabled(True)

        #-----------------------------------------------------------------------
        # Home Motor
        #-----------------------------------------------------------------------

        GPIO.setmode(GPIO.BCM)
        GPIO_PIR = 4

        GPIO.setup(GPIO_PIR, GPIO.IN, pull_up_down = GPIO.PUD_UP)

        #if GPIO_PIR == GPIO.HIGH:
            #tmc.runToPositionSteps(100) 
        
        while GPIO.input(GPIO_PIR) == GPIO.LOW:
            self.tmc.makeAStep()
            time.sleep(0.002)
            step = self.tmc.getCurrentPosition()
            step = step + 1
            self.tmc.setCurrentPosition(step)
            #print(self.tmc.getCurrentPosition())
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
            #print(self.tmc.getCurrentPosition())
        
        for x in range(35):
            self.tmc.makeAStep()
            time.sleep(0.008)
            
        time.sleep(0.2)    
        self.tmc.setCurrentPosition(0)


        self.tmc.setDirection_reg(0)

        #-----------------------------------------------------------------------
        # deactivate the motor current output
        #-----------------------------------------------------------------------
        self.tmc.setMotorEnabled(False)

        #print("---\n---")

        #-----------------------------------------------------------------------
        # deinitiate the TMC_2209 class
        #-----------------------------------------------------------------------
        #del self.tmc

        #print("---")
        print("BoxController - Motor Homed")
        #print("---")

        try:
            del self.tmc
        except:
            pass
        
        #try:
            #cleanup GPIO if it exists.
            #GPIO.cleanup()
        #except:
        #    pass
        
        return True

    def DeployIndex(self, index):
        
        self.tmc = TMC_2209(16, 20, 21)


        #-----------------------------------------------------------------------
        # set the loglevel of the libary (currently only printed)
        # set whether the movement should be relative or absolute
        # both optional
        #-----------------------------------------------------------------------
        self.tmc.setLoglevel(Loglevel.none)
        self.tmc.setMovementAbsRel(MovementAbsRel.absolute)

        #-----------------------------------------------------------------------
        # these functions change settings in the TMC register
        #-----------------------------------------------------------------------
        self.tmc.setDirection_reg(False)
        self.tmc.setVSense(True)
        self.tmc.setCurrent(600)
        self.tmc.setIScaleAnalog(True)
        self.tmc.setInterpolation(True)
        self.tmc.setSpreadCycle(False)
        self.tmc.setMicrosteppingResolution(2)
        self.tmc.setInternalRSense(False)


        #print("---\n---")

        #-----------------------------------------------------------------------
        # these functions read and print the current settings in the TMC register
        #-----------------------------------------------------------------------
        self.tmc.readIOIN()
        self.tmc.readCHOPCONF()
        self.tmc.readDRVSTATUS()
        self.tmc.readGCONF()

        #print("---\n---")

        #-----------------------------------------------------------------------
        # set the Accerleration and maximal Speed
        #-----------------------------------------------------------------------
        self.tmc.setAcceleration(2000)
        self.tmc.setMaxSpeed(500)
        
        GPIO.setmode(GPIO.BCM)
        GPIO_PIR = 4

        GPIO.setup(GPIO_PIR, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        
        if index >= 0 and index <= 6:
            print("BoxController - To Index = ", index)
            self.tmc.setMotorEnabled(True)
            self.DecideReverse(933 * index)
            print(self.tmc.getCurrentPosition())
            time.sleep(0.5)
            self.tmc.setMotorEnabled(False)
            return True
        else:
            print("BoxController - Index out of Range!")
            return False
    
    def DecideReverse(self,step): 
        current = self.tmc.getCurrentPosition()
        #current index 4
        # 933 * 3
        
        #index 3?
        #absolute value of current - step
        #

        if current > step:
            print(current, step)
            self.tmc.setDirection_pin(0)
            self.tmc.runToPositionSteps(step)
        else:
            print(current, step)
            self.tmc.setDirection_pin(1)
            self.tmc.runToPositionSteps(step)
           
    def OpenSlot(self):
        self.aservo = MyServo()
        print("BoxController - Servo created.")
        self.tmc.setMotorEnabled(True)
        self.aservo.ActivateServo("open", 0)
        time.sleep(5)
        del self.aservo
        

    def CloseSlot(self):
        self.aservo = MyServo()
        print("BoxController - Servo created.")
        self.aservo.ActivateServo("close", 0)
        time.sleep(1)
        self.tmc.setMotorEnabled(False)
        #try:
        #    del self.tmc
        #    del self.aservo
        #except:
        #    pass

    '''def __del__(self):
        print("aservo deleted")
        self.aservo.close()'''

if __name__ == "__main__":
    
    command = Stepper()
    
    #command.HomeStepper()
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
