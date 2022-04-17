'''https://github.com/Chr157i4n/TMC2209_Raspberry_Pi'''

from .TMC_2209_uart import TMC_UART
from . import TMC_2209_reg as reg
import RPi.GPIO as GPIO
import time
from enum import Enum
import math
import statistics



class Direction(Enum):
    CCW = 0
    CW = 1


class Loglevel(Enum):
    none = 0
    error = 10
    info = 20
    debug = 30
    movement = 40
    all = 100


class MovementAbsRel(Enum):
    absolute = 0
    relative = 1
    




#-----------------------------------------------------------------------
# TMC_2209
#
# this class has two different functions:
# 1. change setting in the TMC-driver via UART
# 2. move the motor via STEP/DIR pins
#-----------------------------------------------------------------------
class TMC_2209:
    
    tmc_uart = None
    _pin_step = -1
    _pin_dir = -1
    _pin_en = -1

    _direction = True

    _stop = False

    _msres = -1
    _stepsPerRevolution = 0
    
    _loglevel = Loglevel.info

    _currentPos = 0                 # current position of stepper in steps
    _targetPos = 0                  # the target position in steps
    _speed = 0.0                    # the current speed in steps per second
    _maxSpeed = 1.0                 # the maximum speed in steps per second
    _maxSpeedHoming = 500           # the maximum speed in steps per second for homing
    _acceleration = 1.0             # the acceleration in steps per second per second
    _accelerationHoming = 10000     # the acceleration in steps per second per second for homing
    _sqrt_twoa = 1.0                # Precomputed sqrt(2*_acceleration)
    _stepInterval = 0               # the current interval between two steps
    _minPulseWidth = 1              # minimum allowed pulse with in microseconds
    _lastStepTime = 0               # The last step time in microseconds
    _n = 0                          # step counter
    _c0 = 0                         # Initial step size in microseconds
    _cn = 0                         # Last step size in microseconds
    _cmin = 0                       # Min step size in microseconds based on maxSpeed
    _sg_threshold = 100             # threshold for stallguard
    _movement_abs_rel = MovementAbsRel.absolute
    
    
#-----------------------------------------------------------------------
# constructor
#-----------------------------------------------------------------------
    def __init__(self, pin_step, pin_dir, pin_en, baudrate=115200, serialport="/dev/serial0"):
        self.tmc_uart = TMC_UART(serialport, baudrate)
        self._pin_step = pin_step
        self._pin_dir = pin_dir
        self._pin_en = pin_en
        if(self._loglevel.value >= Loglevel.info.value):
            pass
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._pin_step, GPIO.OUT)
        GPIO.setup(self._pin_dir, GPIO.OUT)
        GPIO.setup(self._pin_en, GPIO.OUT)
        GPIO.output(self._pin_dir, self._direction)
        if(self._loglevel.value >= Loglevel.info.value):
            pass
        self.readStepsPerRevolution()
        self.clearGSTAT()
        self.tmc_uart.flushSerialBuffer()
        if(self._loglevel.value >= Loglevel.info.value):
            pass


#-----------------------------------------------------------------------
# destructor
#-----------------------------------------------------------------------
    def __del__(self):
        if(self._loglevel.value >= Loglevel.info.value):
            pass
        self.setMotorEnabled(False)
        GPIO.cleanup((self._pin_step, self._pin_dir, self._pin_en))


#-----------------------------------------------------------------------
# set the loglevel. See the Enum Loglevel
#-----------------------------------------------------------------------       
    def setLoglevel(self, loglevel):
        self._loglevel = loglevel


#-----------------------------------------------------------------------
# set whether the movment should be relative or absolute by default.
# See the Enum MovementAbsoluteRelative
#-----------------------------------------------------------------------       
    def setMovementAbsRel(self, movement_abs_rel):
        self._movement_abs_rel = movement_abs_rel





#-----------------------------------------------------------------------
# read the register Adress "DRVSTATUS" and pass
#-----------------------------------------------------------------------
    def readDRVSTATUS(self):
        pass
        pass
        drvstatus =self.tmc_uart.read_int(reg.DRVSTATUS)
        if(self._loglevel.value >= Loglevel.info.value):
            pass
        if(drvstatus & reg.stst):
            pass
        else:
            pass

        if(drvstatus & reg.stealth):
            pass
        else:
            pass

        cs_actual = drvstatus & reg.cs_actual
        cs_actual = cs_actual >> 16
        pass

        if(drvstatus & reg.olb):
            pass
        
        if(drvstatus & reg.ola):
            pass
        
        if(drvstatus & reg.s2vsb):
            pass

        if(drvstatus & reg.s2vsa):
            pass

        if(drvstatus & reg.s2gb):
            pass
        
        if(drvstatus & reg.s2ga):
            pass
        
        if(drvstatus & reg.ot):
            pass
        
        if(drvstatus & reg.otpw):
            pass
        
        pass
        return drvstatus
            

#-----------------------------------------------------------------------
# read the register Adress "GCONF" and pass
#-----------------------------------------------------------------------
    def readGCONF(self):
        pass
        pass
        gconf = self.tmc_uart.read_int(reg.GCONF)
        if(self._loglevel.value >= Loglevel.info.value):
            pass

        if(gconf & reg.i_scale_analog):
            pass
        else:
            pass
        if(gconf & reg.internal_rsense):
            pass
            pass
            pass
            raise SystemExit
        else:
            pass
        if(gconf & reg.en_spreadcycle):
            pass
        else:
            pass
        if(gconf & reg.shaft):
            pass
        else:
            pass
        if(gconf & reg.index_otpw):
            pass
        else:
            pass
        if(gconf & reg.index_step):
            pass
        else:
            pass
        if(gconf & reg.mstep_reg_select):
            pass
        else:
            pass
        
        pass
        return gconf


#-----------------------------------------------------------------------
# read the register Adress "GSTAT" and pass
#-----------------------------------------------------------------------
    def readGSTAT(self):
        pass
        pass
        gstat = self.tmc_uart.read_int(reg.GSTAT)
        if(self._loglevel.value >= Loglevel.info.value):
            pass
        if(gstat & reg.reset):
            pass
        if(gstat & reg.drv_err):
            pass
        if(gstat & reg.uv_cp):
            pass
        pass
        return gstat


#-----------------------------------------------------------------------
# read the register Adress "GSTAT" and pass
#-----------------------------------------------------------------------
    def clearGSTAT(self):        
        gstat = self.tmc_uart.read_int(reg.GSTAT)
        
        gstat = self.tmc_uart.set_bit(gstat, reg.reset)
        gstat = self.tmc_uart.set_bit(gstat, reg.drv_err)
        
        self.tmc_uart.write_reg_check(reg.GSTAT, gstat)

 
#-----------------------------------------------------------------------
# read the register Adress "IOIN" and pass
#-----------------------------------------------------------------------
    def readIOIN(self):
        pass
        pass
        ioin = self.tmc_uart.read_int(reg.IOIN)
        if(self._loglevel.value >= Loglevel.info.value):
            pass
        if(ioin & reg.io_spread):
            pass
        else:
            pass

        if(ioin & reg.io_dir):
            pass
        else:
            pass

        if(ioin & reg.io_step):
            pass
        else:
            pass

        if(ioin & reg.io_enn):
            pass
        else:
            pass
        
        pass
        return ioin


#-----------------------------------------------------------------------
# read the register Adress "CHOPCONF" and pass
#-----------------------------------------------------------------------
    def readCHOPCONF(self):
        pass
        pass
        chopconf = self.tmc_uart.read_int(reg.CHOPCONF)
        if(self._loglevel.value >= Loglevel.info.value):
            pass
        
        pass
        
        if(chopconf & reg.intpol):
            pass
        
        if(chopconf & reg.vsense):
            pass
        else:
            pass

        pass
        return chopconf





#-----------------------------------------------------------------------
# enables or disables the motor current output
#-----------------------------------------------------------------------
    def setMotorEnabled(self, en):
        GPIO.output(self._pin_en, not en)
        if(self._loglevel.value >= Loglevel.info.value):
            pass
      

#-----------------------------------------------------------------------
# homes the motor in the given direction using stallguard
#-----------------------------------------------------------------------
    def doHoming(self, direction, threshold=None):
        sg_results = []
        
        if(threshold is not None):
            self._sg_threshold = threshold
        
        if(self._loglevel.value >= Loglevel.info.value):
            pass
            pass
        
        if(self._loglevel.value >= Loglevel.debug.value):
            pass
        
        self.setDirection_pin(direction)
        self.setSpreadCycle(0)

        if (direction == 1):
            self._targetPos = self._stepsPerRevolution * 10
        else:
            self._targetPos = -self._stepsPerRevolution * 10
        self._stepInterval = 0
        self._speed = 0.0
        self._n = 0
        self.setAcceleration(10000)
        self.setMaxSpeed(self._maxSpeedHoming)
        self.computeNewSpeed()


        step_counter=0
        #pass
        while (step_counter<self._stepsPerRevolution):
            if (self.runSpeed()): #returns true, when a step is made
                step_counter += 1
                self.computeNewSpeed()
                sg_result = self.getStallguard_Result()
                sg_results.append(sg_result)
                if(len(sg_results)>20):
                    sg_result_average = statistics.mean(sg_results[-6:])
                    if(sg_result_average < self._sg_threshold):
                        break

        if(step_counter<self._stepsPerRevolution):
            if(self._loglevel.value >= Loglevel.info.value):
                pass
                pass
            if(self._loglevel.value >= Loglevel.debug.value):
                pass
                pass
            self._currentPos = 0
        else:
            if(self._loglevel.value >= Loglevel.error.value):
                pass
            if(self._loglevel.value >= Loglevel.debug.value):
                pass
                pass
        
        if(self._loglevel.value >= Loglevel.info.value):
            pass
        

#-----------------------------------------------------------------------
# returns the current motor position in microsteps
#-----------------------------------------------------------------------
    def getCurrentPosition(self):
        return self._currentPos


#-----------------------------------------------------------------------
# overwrites the current motor position in microsteps
#-----------------------------------------------------------------------
    def setCurrentPosition(self, newPos):
        self._currentPos = newPos

       
#-----------------------------------------------------------------------
# reverses the motor shaft direction
#-----------------------------------------------------------------------
    def reverseDirection_pin(self):
        self._direction = not self._direction
        GPIO.output(self._pin_dir, self.direction)


#-----------------------------------------------------------------------
# sets the motor shaft direction to the given value: 0 = CCW; 1 = CW
#-----------------------------------------------------------------------
    def setDirection_pin(self, direction):
        self._direction = direction
        GPIO.output(self._pin_dir, direction)


#-----------------------------------------------------------------------
# returns the motor shaft direction: 0 = CCW; 1 = CW
#-----------------------------------------------------------------------
    def getDirection_reg(self):
        gconf = self.tmc_uart.read_int(reg.GCONF)
        return (gconf & reg.shaft)


#-----------------------------------------------------------------------
# sets the motor shaft direction to the given value: 0 = CCW; 1 = CW
#-----------------------------------------------------------------------
    def setDirection_reg(self, direction):        
        gconf = self.tmc_uart.read_int(reg.GCONF)
        if(direction):
            if(self._loglevel.value >= Loglevel.info.value):
                pass
            gconf = self.tmc_uart.set_bit(gconf, reg.shaft)
        else:
            if(self._loglevel.value >= Loglevel.info.value):
                pass
            gconf = self.tmc_uart.clear_bit(gconf, reg.shaft)
        self.tmc_uart.write_reg_check(reg.GCONF, gconf)
  

#-----------------------------------------------------------------------
# return whether Vref (1) or 5V (0) is used for current scale
#-----------------------------------------------------------------------
    def getIScaleAnalog(self):
        gconf = self.tmc_uart.read_int(reg.GCONF)
        return (gconf & reg.i_scale_analog)


#-----------------------------------------------------------------------
# sets Vref (1) or 5V (0) for current scale
#-----------------------------------------------------------------------
    def setIScaleAnalog(self,en):        
        gconf = self.tmc_uart.read_int(reg.GCONF)
        if(en):
            if(self._loglevel.value >= Loglevel.info.value):
                pass
            gconf = self.tmc_uart.set_bit(gconf, reg.i_scale_analog)
        else:
            if(self._loglevel.value >= Loglevel.info.value):
                pass
            gconf = self.tmc_uart.clear_bit(gconf, reg.i_scale_analog)
        self.tmc_uart.write_reg_check(reg.GCONF, gconf)


#-----------------------------------------------------------------------
# returns which sense resistor voltage is used for current scaling
# 0: Low sensitivity, high sense resistor voltage
# 1: High sensitivity, low sense resistor voltage
#-----------------------------------------------------------------------
    def getVSense(self):
        chopconf = self.tmc_uart.read_int(reg.CHOPCONF)
        return (chopconf & reg.vsense)


#-----------------------------------------------------------------------
# sets which sense resistor voltage is used for current scaling
# 0: Low sensitivity, high sense resistor voltage
# 1: High sensitivity, low sense resistor voltage
#-----------------------------------------------------------------------
    def setVSense(self,en):      
        chopconf = self.tmc_uart.read_int(reg.CHOPCONF)
        if(en):
            if(self._loglevel.value >= Loglevel.info.value):
                pass
            chopconf = self.tmc_uart.set_bit(chopconf, reg.vsense)
        else:
            if(self._loglevel.value >= Loglevel.info.value):
                pass
            chopconf = self.tmc_uart.clear_bit(chopconf, reg.vsense)
        self.tmc_uart.write_reg_check(reg.CHOPCONF, chopconf)


#-----------------------------------------------------------------------
# returns which sense resistor voltage is used for current scaling
# 0: Low sensitivity, high sense resistor voltage
# 1: High sensitivity, low sense resistor voltage
#-----------------------------------------------------------------------
    def getInternalRSense(self):
        gconf = self.tmc_uart.read_int(reg.GCONF)
        return (gconf & reg.internal_rsense)


#-----------------------------------------------------------------------
# sets which sense resistor voltage is used for current scaling
# 0: Low sensitivity, high sense resistor voltage
# 1: High sensitivity, low sense resistor voltage
#-----------------------------------------------------------------------
    def setInternalRSense(self,en):        
        gconf = self.tmc_uart.read_int(reg.GCONF)
        if(en):
            if(self._loglevel.value >= Loglevel.info.value):
                pass
            gconf = self.tmc_uart.set_bit(gconf, reg.internal_rsense)
        else:
            if(self._loglevel.value >= Loglevel.info.value):
                pass
            gconf = self.tmc_uart.clear_bit(gconf, reg.internal_rsense)
        self.tmc_uart.write_reg_check(reg.GCONF, gconf)
    

#-----------------------------------------------------------------------
# sets the current scale (CS) for Running and Holding
# and the delay, when to be switched to Holding current
# IHold = 0-31; IRun = 0-31; IHoldDelay = 0-15
#-----------------------------------------------------------------------
    def setIRun_Ihold(self, IHold, IRun, IHoldDelay):
        ihold_irun = 0
        
        ihold_irun = ihold_irun | IHold << 0
        ihold_irun = ihold_irun | IRun << 8
        ihold_irun = ihold_irun | IHoldDelay << 16
        if(self._loglevel.value >= Loglevel.info.value):
            pass
            pass

            pass
        self.tmc_uart.write_reg_check(reg.IHOLD_IRUN, ihold_irun)


#-----------------------------------------------------------------------
# sets the current flow for the motor
# run_current in mA
# check whether Vref is actually 1.2V
#-----------------------------------------------------------------------
    def setCurrent(self, run_current, hold_current_multiplier = 0.5, hold_current_delay = 10, Vref = 1.2):
        CS_IRun = 0
        Rsense = 0.11
        Vfs = 0

        if(self.getVSense()):
            if(self._loglevel.value >= Loglevel.info.value):
                pass
            Vfs = 0.180 * Vref / 2.5
        else:
            if(self._loglevel.value >= Loglevel.info.value):
                pass
            Vfs = 0.325 * Vref / 2.5
            
        CS_IRun = 32.0*1.41421*run_current/1000.0*(Rsense+0.02)/Vfs - 1

        CS_IRun = min(CS_IRun, 31)
        CS_IRun = max(CS_IRun, 0)
        
        CS_IHold = hold_current_multiplier * CS_IRun

        CS_IRun = round(CS_IRun)
        CS_IHold = round(CS_IHold)
        hold_current_delay = round(hold_current_delay)

        if(self._loglevel.value >= Loglevel.info.value):
            pass
            pass
            pass

        self.setIRun_Ihold(CS_IHold, CS_IRun, hold_current_delay)

  
#-----------------------------------------------------------------------
# return whether spreadcycle (1) is active or stealthchop (0)
#-----------------------------------------------------------------------
    def getSpreadCycle(self):
        gconf = self.tmc_uart.read_int(reg.GCONF)
        return (gconf & reg.en_spreadcycle)


#-----------------------------------------------------------------------
# enables spreadcycle (1) or stealthchop (0)
#-----------------------------------------------------------------------
    def setSpreadCycle(self,en_spread):
        gconf = self.tmc_uart.read_int(reg.GCONF)
        if(en_spread):
            if(self._loglevel.value >= Loglevel.info.value):
                pass
            gconf = self.tmc_uart.set_bit(gconf, reg.en_spreadcycle)
        else:
            if(self._loglevel.value >= Loglevel.info.value):
                pass
            gconf = self.tmc_uart.clear_bit(gconf, reg.en_spreadcycle)
        self.tmc_uart.write_reg_check(reg.GCONF, gconf)


#-----------------------------------------------------------------------
# return whether the tmc inbuilt interpolation is active
#-----------------------------------------------------------------------
    def getInterpolation(self):
        chopconf = self.tmc_uart.read_int(reg.CHOPCONF)
        if(chopconf & reg.intpol):
            return True
        else:
            return False

    
#-----------------------------------------------------------------------
# enables the tmc inbuilt interpolation of the steps to 256 microsteps
#-----------------------------------------------------------------------
    def setInterpolation(self, en):
        chopconf = self.tmc_uart.read_int(reg.CHOPCONF)

        if(en):
            chopconf = self.tmc_uart.set_bit(chopconf, reg.intpol)
        else:
            chopconf = self.tmc_uart.clear_bit(chopconf, reg.intpol)

        if(self._loglevel.value >= Loglevel.info.value):
            pass
        self.tmc_uart.write_reg_check(reg.CHOPCONF, chopconf)


#-----------------------------------------------------------------------
# returns the current native microstep resolution (1-256)
#-----------------------------------------------------------------------
    def getMicroSteppingResolution(self):
        chopconf = self.tmc_uart.read_int(reg.CHOPCONF)
        
        msresdezimal = chopconf & (reg.msres0 | reg.msres1 | reg.msres2 | reg.msres3)
        
        msresdezimal = msresdezimal >> 24
        msresdezimal = 8 - msresdezimal
                
        self._msres = int(math.pow(2, msresdezimal))
        
        return self._msres


#-----------------------------------------------------------------------
# sets the current native microstep resolution (1,2,4,8,16,32,64,128,256)
#-----------------------------------------------------------------------
    def setMicrosteppingResolution(self, msres):      
        chopconf = self.tmc_uart.read_int(reg.CHOPCONF)
        chopconf = chopconf & (~reg.msres0 | ~reg.msres1 | ~reg.msres2 | ~reg.msres3) #setting all bits to zero
        msresdezimal = int(math.log(msres, 2))
        msresdezimal = 8 - msresdezimal
        chopconf = int(chopconf) & int(4043309055)
        chopconf = chopconf | msresdezimal <<24
        
        if(self._loglevel.value >= Loglevel.info.value):
            pass
        self.tmc_uart.write_reg_check(reg.CHOPCONF, chopconf)
        
        self.setMStepResolutionRegSelect(True)

        self.readStepsPerRevolution()

        return True
        

#-----------------------------------------------------------------------
# sets the register bit "mstep_reg_select" to 1 or 0 depending to the given value.
# this is needed to set the microstep resolution via UART
# this method is called by "setMicrosteppingResolution"
#-----------------------------------------------------------------------
    def setMStepResolutionRegSelect(self, en):                  
        gconf = self.tmc_uart.read_int(reg.GCONF)
        
        if(en == True):
            gconf = self.tmc_uart.set_bit(gconf, reg.mstep_reg_select)
        else:
            gconf = self.tmc_uart.clear_bit(gconf, reg.mstep_reg_select)

        if(self._loglevel.value >= Loglevel.info.value):
            pass
        self.tmc_uart.write_reg_check(reg.GCONF, gconf)
        

#-----------------------------------------------------------------------
# returns how many steps are needed for one revolution
#-----------------------------------------------------------------------
    def readStepsPerRevolution(self):
        self._stepsPerRevolution = 200*self.getMicroSteppingResolution()
        return self._stepsPerRevolution


#-----------------------------------------------------------------------
# returns how many steps are needed for one revolution
#-----------------------------------------------------------------------
    def getStepsPerRevolution(self):
        return self._stepsPerRevolution


#-----------------------------------------------------------------------
# reads the interface transmission counter from the tmc register
# this value is increased on every succesfull write access
# can be used to verify a write access
#-----------------------------------------------------------------------
    def getInterfaceTransmissionCounter(self):
        ifcnt = self.tmc_uart.read_int(reg.IFCNT)
        if(self._loglevel.value >= Loglevel.debug.value):
            pass
        return ifcnt


#-----------------------------------------------------------------------
# return the current stallguard result
# its will be calculated with every fullstep
# higher values means a lower motor load
#-----------------------------------------------------------------------
    def getTStep(self):
        tstep = self.tmc_uart.read_int(reg.TSTEP)
        return tstep


#-----------------------------------------------------------------------
# sets the register bit "VACTUAL" to to a given value
# VACTUAL allows moving the motor by UART control.
# It gives the motor velocity in +-(2^23)-1 [μsteps / t]
# 0: Normal operation. Driver reacts to STEP input
#-----------------------------------------------------------------------
    def setVActual(self, vactual):
        if(self._loglevel.value >= Loglevel.info.value):
            pass
            pass

            pass
        self.tmc_uart.write_reg_check(reg.VACTUAL, vactual)


#-----------------------------------------------------------------------
# return the current stallguard result
# its will be calculated with every fullstep
# higher values means a lower motor load
#-----------------------------------------------------------------------
    def getStallguard_Result(self):
        sg_result = self.tmc_uart.read_int(reg.SG_RESULT)
        return sg_result


#-----------------------------------------------------------------------
# sets the register bit "SGTHRS" to to a given value
# this is needed for the stallguard interrupt callback
# SG_RESULT becomes compared to the double of this threshold.
# SG_RESULT ≤ SGTHRS*2
#-----------------------------------------------------------------------
    def setStallguard_Threshold(self, threshold):

        if(self._loglevel.value >= Loglevel.info.value):
            pass
            pass

            pass
        self.tmc_uart.write_reg_check(reg.SGTHRS, threshold)


#-----------------------------------------------------------------------
# This  is  the  lower  threshold  velocity  for  switching  
# on  smart energy CoolStep and StallGuard to DIAG output. (unsigned)
#-----------------------------------------------------------------------
    def setCoolStep_Threshold(self, threshold):

        if(self._loglevel.value >= Loglevel.info.value):
            pass
            pass

            pass
        self.tmc_uart.write_reg_check(reg.TCOOLTHRS, threshold)


#-----------------------------------------------------------------------
# set a function to call back, when the driver detects a stall 
# via stallguard
# high value on the diag pin can also mean a driver error
#-----------------------------------------------------------------------
    def setStallguard_Callback(self, pin_stallguard, threshold, my_callback, min_speed = 2000):

        self.setStallguard_Threshold(threshold)
        self.setCoolStep_Threshold(min_speed)

        if(self._loglevel.value >= Loglevel.info.value):
            pass
        
        GPIO.setup(pin_stallguard, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
        GPIO.add_event_detect(pin_stallguard, GPIO.RISING, callback=my_callback, bouncetime=300) 



#-----------------------------------------------------------------------
# returns the current Microstep counter.
# Indicates actual position in the microstep table for CUR_A
#-----------------------------------------------------------------------
    def getMicrostepCounter(self):
        mscnt = self.tmc_uart.read_int(reg.MSCNT)
        return mscnt


#-----------------------------------------------------------------------
# returns the current Microstep counter.
# Indicates actual position in the microstep table for CUR_A
#-----------------------------------------------------------------------
    def getMicrostepCounterInSteps(self, offset=0):
        step = (self.getMicrostepCounter()-64)*(self._msres*4)/1024
        step = (4*self._msres)-step-1
        step = round(step)
        return step+offset


#-----------------------------------------------------------------------
# sets the maximum motor speed in steps per second
#-----------------------------------------------------------------------
    def setMaxSpeed(self, speed):
        if (speed < 0.0):
           speed = -speed
        if (self._maxSpeed != speed):
            self._maxSpeed = speed
            self._cmin = 1000000.0 / speed
            # Recompute _n from current speed and adjust speed if accelerating or cruising
            if (self._n > 0):
                self._n = (self._speed * self._speed) / (2.0 * self._acceleration) # Equation 16
                self.computeNewSpeed()


#-----------------------------------------------------------------------
# returns the maximum motor speed in steps per second
#-----------------------------------------------------------------------
    def getMaxSpeed(self):
        return self._maxSpeed


#-----------------------------------------------------------------------
# sets the motor acceleration/decceleration in steps per sec per sec
#-----------------------------------------------------------------------
    def setAcceleration(self, acceleration):
        if (acceleration == 0.0):
            return
        if (acceleration < 0.0):
          acceleration = -acceleration
        if (self._acceleration != acceleration):
            # Recompute _n per Equation 17
            self._n = self._n * (self._acceleration / acceleration)
            # New c0 per Equation 7, with correction per Equation 15
            self._c0 = 0.676 * math.sqrt(2.0 / acceleration) * 1000000.0 # Equation 15
            self._acceleration = acceleration
            self.computeNewSpeed()


#-----------------------------------------------------------------------
# returns the motor acceleration/decceleration in steps per sec per sec
#-----------------------------------------------------------------------
    def getAcceleration(self):
        return self._acceleration


#-----------------------------------------------------------------------
# stop the current movement
#-----------------------------------------------------------------------
    def stop(self):
        self._stop = True


#-----------------------------------------------------------------------
# runs the motor to the given position.
# with acceleration and deceleration
# blocks the code until finished or stopped from a different thread!
# returns true when the movement if finshed normally and false,
# when the movement was stopped
#-----------------------------------------------------------------------
    def runToPositionSteps(self, steps, movement_abs_rel = None):
        if(movement_abs_rel is not None):
            this_movement_abs_rel = movement_abs_rel
        else:
            this_movement_abs_rel = self._movement_abs_rel

        if(this_movement_abs_rel == MovementAbsRel.relative):
            self._targetPos = self._currentPos + steps
        else:
            self._targetPos = steps

        self._stop = False
        self._stepInterval = 0
        self._speed = 0.0
        self._n = 0
        self.computeNewSpeed()
        while (self.run() and not self._stop): #returns false, when target position is reached
            pass
        return not self._stop


#-----------------------------------------------------------------------
# runs the motor to the given position.
# with acceleration and deceleration
# blocks the code until finished!
#-----------------------------------------------------------------------
    def runToPositionRevolutions(self, revolutions, movement_absolute_relative = None):
        return self.runToPositionSteps(round(revolutions * self._stepsPerRevolution), movement_absolute_relative)


#-----------------------------------------------------------------------
# calculates a new speed if a speed was made
# returns true if the target position is reached
# should not be called from outside!
#-----------------------------------------------------------------------
    def run(self):
        if (self.runSpeed()): #returns true, when a step is made
            self.computeNewSpeed()
            #pass
            #pass
        return (self._speed != 0.0 and self.distanceToGo() != 0)


#-----------------------------------------------------------------------
# returns the remaining distance the motor should run
#-----------------------------------------------------------------------
    def distanceToGo(self):
        return self._targetPos - self._currentPos


#-----------------------------------------------------------------------
# returns the calculated current speed depending on the acceleration
# this code is based on: 
# "Generate stepper-motor speed profiles in real time" by David Austin
#
# https://www.embedded.com/generate-stepper-motor-speed-profiles-in-real-time/
# https://web.archive.org/web/20140705143928/http://fab.cba.mit.edu/classes/MIT/961.09/projects/i0/Stepper_Motor_Speed_Profile.pdf
#-----------------------------------------------------------------------
    def computeNewSpeed(self):
        distanceTo = self.distanceToGo() # +ve is clockwise from curent location
        stepsToStop = (self._speed * self._speed) / (2.0 * self._acceleration) # Equation 16
        if (distanceTo == 0 and stepsToStop <= 1):
            # We are at the target and its time to stop
            self._stepInterval = 0
            self._speed = 0.0
            self._n = 0
            if(self._loglevel.value >= Loglevel.movement.value):
                pass
            return
        
        if (distanceTo > 0):
            # We are anticlockwise from the target
            # Need to go clockwise from here, maybe decelerate now
            if (self._n > 0):
                # Currently accelerating, need to decel now? Or maybe going the wrong way?
                if ((stepsToStop >= distanceTo) or self._direction == Direction.CCW):
                    self._n = -stepsToStop # Start deceleration
            elif (self._n < 0):
                # Currently decelerating, need to accel again?
                if ((stepsToStop < distanceTo) and self._direction == Direction.CW):
                    self._n = -self._n # Start accceleration
        elif (distanceTo < 0):
            # We are clockwise from the target
            # Need to go anticlockwise from here, maybe decelerate
            if (self._n > 0):
                # Currently accelerating, need to decel now? Or maybe going the wrong way?
                if ((stepsToStop >= -distanceTo) or self._direction == Direction.CW):
                    self._n = -stepsToStop # Start deceleration
            elif (self._n < 0):
                # Currently decelerating, need to accel again?
                if ((stepsToStop < -distanceTo) and self._direction == Direction.CCW):
                    self._n = -self._n # Start accceleration
        # Need to accelerate or decelerate
        if (self._n == 0):
            # First step from stopped
            self._cn = self._c0
            GPIO.output(self._pin_step, GPIO.LOW)
            #pass
            if(distanceTo > 0):
                self.setDirection_pin(1)
                if(self._loglevel.value >= Loglevel.movement.value):
                    pass
            else:
                self.setDirection_pin(0)
                if(self._loglevel.value >= Loglevel.movement.value):
                    pass
        else:
            # Subsequent step. Works for accel (n is +_ve) and decel (n is -ve).
            self._cn = self._cn - ((2.0 * self._cn) / ((4.0 * self._n) + 1)) # Equation 13
            self._cn = max(self._cn, self._cmin)
        self._n += 1
        self._stepInterval = self._cn
        self._speed = 1000000.0 / self._cn
        if (self._direction == 0):
            self._speed = -self._speed


#-----------------------------------------------------------------------
# this methods does the actual steps with the current speed
#-----------------------------------------------------------------------
    def runSpeed(self):
        # Dont do anything unless we actually have a step interval
        if (not self._stepInterval):
            return False
        
        curtime = time.time_ns()/1000
        
        #pass
        #pass
        
        if (curtime - self._lastStepTime >= self._stepInterval):

            if (self._direction == 1): # Clockwise
                self._currentPos += 1
            else: # Anticlockwise 
                self._currentPos -= 1
            self.makeAStep()
            
            self._lastStepTime = curtime # Caution: does not account for costs in step()
            return True
        else:
            return False



#-----------------------------------------------------------------------
# method that makes on step
# for the TMC2209 there needs to be a signal duration of minimum 100 ns
#-----------------------------------------------------------------------
    def makeAStep(self):
        GPIO.output(self._pin_step, GPIO.HIGH)
        time.sleep(1/1000/1000)
        GPIO.output(self._pin_step, GPIO.LOW)
        time.sleep(1/1000/1000)

        if(self._loglevel.value >= Loglevel.movement.value):
                pass


#-----------------------------------------------------------------------
# tests the EN, DIR and STEP pin
# this sets the EN, DIR and STEP pin to HIGH, LOW and HIGH
# and checks the IOIN Register of the TMC meanwhile
#-----------------------------------------------------------------------
    def testDirStepEn(self):
        pin_dir_ok = pin_step_ok = pin_en_ok = True
        
        GPIO.output(self._pin_step, GPIO.HIGH)
        GPIO.output(self._pin_dir, GPIO.HIGH)
        GPIO.output(self._pin_en, GPIO.HIGH)
        time.sleep(0.1)
        ioin = self.readIOIN()
        if(not(ioin & reg.io_dir)):
            pin_dir_ok = False
        if(not(ioin & reg.io_step)):
            pin_step_ok = False
        if(not(ioin & reg.io_enn)):
            pin_en_ok = False

        GPIO.output(self._pin_step, GPIO.LOW)
        GPIO.output(self._pin_dir, GPIO.LOW)
        GPIO.output(self._pin_en, GPIO.LOW)
        time.sleep(0.1)
        ioin = self.readIOIN()
        if(ioin & reg.io_dir):
            pin_dir_ok = False
        if(ioin & reg.io_step):
            pin_step_ok = False
        if(ioin & reg.io_enn):
            pin_en_ok = False

        GPIO.output(self._pin_step, GPIO.HIGH)
        GPIO.output(self._pin_dir, GPIO.HIGH)
        GPIO.output(self._pin_en, GPIO.HIGH)
        time.sleep(0.1)
        ioin = self.readIOIN()
        if(not(ioin & reg.io_dir)):
            pin_dir_ok = False
        if(not(ioin & reg.io_step)):
            pin_step_ok = False
        if(not(ioin & reg.io_enn)):
            pin_en_ok = False

        self.setMotorEnabled(False)

        pass
        if(pin_dir_ok):
            pass
        else:
            pass
        if(pin_step_ok):
            pass
        else:
            pass
        if(pin_en_ok):
            pass
        else:
            pass
        pass


#-----------------------------------------------------------------------
# test method
#-----------------------------------------------------------------------
    def test(self):
        self.setDirection_pin(1)
        
        for i in range(100):
            self._currentPos += 1
            GPIO.output(self._pin_step, GPIO.HIGH)
            time.sleep(0.001)
            GPIO.output(self._pin_step, GPIO.LOW)
            time.sleep(0.01)