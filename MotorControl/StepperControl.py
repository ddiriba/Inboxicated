from TMC_2209.TMC_2209_StepperDriver import *
from spitest import *
import time

tmc = TMC_2209(16, 20, 21)

tmc.setLoglevel(Loglevel.none)
tmc.setMovementAbsRel(MovementAbsRel.absolute)

tmc.setDirection_reg(False)
tmc.setVSense(True)
tmc.setCurrent(150)
tmc.setIScaleAnalog(True)
tmc.setInterpolation(True)
tmc.setSpreadCycle(False)
tmc.setMicrosteppingResolution(2)
tmc.setInternalRSense(False)

tmc.readIOIN()
tmc.readCHOPCONF()
tmc.readDRVSTATUS()
tmc.readGCONF()

tmc.setAcceleration(2000)
tmc.setMaxSpeed(500)

tmc.setMotorEnabled(True)
as5600 = Encoder()



#-----------------------------------------------------------------------
# move the motor 1 revolution
#-----------------------------------------------------------------------

while (Encoder.ReadRawAngle() is not 0.0):

    for x in range (0, 36000, 3):
        tmc.runToPositionSteps(x)                             #move to position 400
        if (Encoder.ReadRawAngle() is 0.0):
            break
        #tmc.runToPositionSteps(0)                               #move to position 0

tmc.setMotorEnabled(False)



#-----------------------------------------------------------------------
# deinitiate the TMC_2209 class
#-----------------------------------------------------------------------
del tmc
