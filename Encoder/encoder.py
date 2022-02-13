# Kristina Nemeth (kan57) & Cuyler Crandall (csc254)
# ECE 5725 Final Project


'''
Ribbon Cable Pinout
Red 1 - VCC 3.3V => Raspberry Pi pin 1
================================= 2 - out (not used, PWM /Analog voltage output)
3 - GND => Raspberry Pi pin 6,9,14,20,25,30,34,or 39
4 - DIR -> connect to ground 6,9,14,20,25,30,34,or 39
5 - SCL => Raspberry Pi pin 5
6 - SDA => Raspberry Pi pin 3
================================= 7 - GPO (not used, for programming)

'''

import time
import spidev
import numpy as math
import RPi.GPIO as GPIO
import ast #For ast.literal_eval to read the config files
import os

#ADC SPI is on SPI channel 2 not 0 for some reason.
spi_ch = 2

# Enable SPI 1 since the TFT is on 0
spi = spidev.SpiDev(0, spi_ch)
spi.max_speed_hz = 120000

#Code is based on the code found in Reference 9 on the project report
def read_adc(adc_ch, vref = 5):
  # Make sure ADC channel is 0 or 1
  if adc_ch != 0:        
    adc_ch = 1
  # Construct SPI message
  #  First bit (Start): Logic high (1)
  #  Second bit (SGL/DIFF): 1 to select single mode
  #  Third bit (ODD/SIGN): Select channel (0 or 1)
  #  Fourth bit (MSFB): 0 for LSB first
  #  Next 12 bits: 0 (don't care)
  msg = 0b11
  msg = ((msg << 1) + adc_ch) << 5
  msg = [msg, 0b00000000]
  reply = spi.xfer2(msg)

  # Construct single integer out of the reply (2 bytes)
  adc = 0
  for n in reply:
    adc = (adc << 8) + n

  # Last bit (0) is not part of ADC value, shift to remove it
  adc = adc >> 1

  # Calculate voltage form ADC value
  voltage = (vref * adc) / 1024
  
  #return voltage
  #Checking if readings are better as just an average of high/low 
  if voltage > 1.5:
    return 1
  else:
    return 0
    
##### Encoder class
class encoder:

  def __init__(self, adcChannel,name):
    self.adcChannel = adcChannel
    self.name = name
    
    #List to store historical ADC readings (for running averages, in V not degrees)
    self.adcReadingHistory = []
    
    #Value of current (assumed) encoder value (deg, not V)
    self.currentReading = 0
    
    self.dir = os.curdir
    
    print(self.dir)
    
    #Tries to pull an initial reading WITH the calibration offset.
    #If no config for calibration exists, instead runs that
    try:
      #Referance voltages at 0 and 90 degrees relative to the system (from config file)
      self.config = ast.literal_eval(open(self.dir+"Config.txt",'r').read())
      #self.V_at0Deg = config.get("reading0deg")
      #self.V_at90deg = config.get("reading90deg")
      #Reference maximum volutage (should be extrapolatable from above values)
      #self.V_max = 0
      self.getReading()
    except:
      print "No config exists for " + self.name + " axis"
      self.calibrate()
      self.config = ast.literal_eval(open(self.dir+"Config.txt",'r').read()) 
      #self.V_at0Deg = config.get("reading0deg")
      #self.V_at90deg = config.get("reading90deg")
      self.getReading()
      
    
  #Pulls a SINGLE ADC datapoint from SPI
  def adcGetData(self):
    self.adcReadingHistory.append(read_adc(self.adcChannel))
    
  #Gets a new reading from the encoder (in degrees)
  #Includes processing for running average, config offset, and larger shifts in angle
  def getReading(self):
  
    #Gets current length of list of readings (to know to clip the running average)
    if self.adcReadingHistory:
      initialLength = len(self.adcReadingHistory)
    else:
      initialLength = 0
      
    #Pull ADC readings for a specified amount of time
    startTime = time.time()
    while time.time() - startTime < 0.5:
      self.adcGetData()
    
    #Checks if new readings are appreciably different from previous readings (>3 degrees)
    #If so, throws out entire reading history prior to this set
    if True or abs(self.currentReading - self.V_to_deg(math.mean(self.adcReadingHistory[initialLength:]))) > 3:
      self.adcReadingHistory = self.adcReadingHistory[initialLength:]
    else:
      #Removes first N readings if N new readings are <10% of reading history
      addedLength = len(self.adcReadingHistory)-initialLength
      if addedLength < 0.1*len(self.adcReadingHistory):
        self.adcReadingHistory = self.adcReadingHistory[addedLength:]
      
    try:  
      #Converts set of voltage readings into a degree reading
      self.currentReading = self.V_to_deg(math.mean(self.adcReadingHistory))
    except:
      print "Cannot set reading until configuration si complete"
    
    print self.name + " Servo is at " + str(round(self.currentReading,2)) + "deg (" + str(round(math.mean(self.adcReadingHistory),2)) + "V, from " + str(round(len(self.adcReadingHistory),2)) + " readings)"
    
    return self.currentReading
    
  #Converts a voltage to a degree reading in system-centric coordinates
  def V_to_deg(self, V):
    #degree = math.remainder((V - self.config.get("reading0deg"))*(90/(self.config.get("reading90deg")-self.config.get("reading0deg"))),360)
    degree = math.remainder((V - self.config.get("reading0deg"))*self.config.get('avgSlope'),360)
    return degree
    
  def clearEncoder(self):
    self.adcReadingHistory = []
  
  #Gets readings at different orientations of the encoder to determine how to translate voltage to degrees  
  def calibrate(self):
    config = open(self.name+"Config.txt","w+")
    print "Now calibrating the " + self.name + "Axis"
    print "Please manually rotate the " + self.name + " Axis to 0deg"
    raw_input("Press ENTER when complete")
    startTime = time.time()
    while time.time() - startTime < 1:
      self.adcGetData()
    reading0deg = round(math.mean(self.adcReadingHistory),3)
    print "0deg Reading: " + str(round(reading0deg,2)) +"V"
    self.clearEncoder()
    print "Please manually rotate the " + self.name + " Axis to 90deg"
    raw_input("Press ENTER when complete")
    startTime = time.time()
    while time.time() - startTime < 1:
      self.adcGetData()
    reading90deg = round(math.mean(self.adcReadingHistory),3)
    print "90deg Reading: " + str(round(reading90deg,2)) +"V"
    self.clearEncoder()
    print "Please manually rotate the " + self.name + " Axis to 180deg"
    raw_input("Press ENTER when complete")
    startTime = time.time()
    while time.time() - startTime < 1:
      self.adcGetData()
    reading180deg = round(math.mean(self.adcReadingHistory),3)
    print "180deg Reading: " + str(round(reading180deg,2)) +"V"
    self.clearEncoder()
    print "Please manually rotate the " + self.name + " Axis to 270deg"
    raw_input("Press ENTER when complete")
    startTime = time.time()
    while time.time() - startTime < 1:
      self.adcGetData()
    reading270deg = round(math.mean(self.adcReadingHistory),3)
    print "270deg Reading: " + str(round(reading270deg,2)) +"V"
    self.clearEncoder()
    
    avgSlope = math.median([(90/(reading90deg-reading0deg)), (90/(reading180deg-reading90deg)), (90/(reading270deg-reading180deg)), (90/(reading0deg-reading270deg))])
    
    readingDict = {'reading0deg':reading0deg, 'reading90deg':reading90deg, 'reading180deg':reading180deg, 'reading270deg':reading270deg, 'avgSlope':avgSlope}
    #config.write("readingsDict" + self.name + " = " + str(readingDict))
    config.write(str(readingDict))
    config.close