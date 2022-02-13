import time
import spidev
import numpy as math
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM) #set up GPIO pins to broadcom setting
GPIO.setup([17], GPIO.IN, pull_up_down=GPIO.PUD_UP) #set up GPIO pins as inputs with pull $
#Defining callbacks for PiTFT buttons
def GPIO17_callback(channel):
  print("Button 17 (Quit) has been pressed")
  GPIO.cleanup()
  exit()
GPIO.add_event_detect(17,GPIO.FALLING,callback=GPIO17_callback,bouncetime=300)

spi_ch = 2

# Enable SPI
spi = spidev.SpiDev(1, spi_ch)
spi.max_speed_hz = 120000

#ADC code is writen based on example code found in write up reference 9
def read_adc(adc_ch, vref = 3.3):

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

    return voltage

# Report the channel 0 and channel 1 voltages to the terminal
try:
    sampleTime = time.time()
    adc_0_list = []
    adc_1_list = []
    adc_0_list_old = 0 #len(adc_0_list)
    adc_1_list_old = 0 #len(adc_1_list)
    #print(len(adc_list_0))
    while True:
        #adc_0 = read_adc(0)
        #adc_1 = read_adc(1)
        adc_0_list.append(read_adc(0))
        adc_1_list.append(read_adc(1))
        #print("Ch 0:", round(adc_0, 2), "V Ch 1:", round(adc_1, 2), "V")
        #time.sleep(0.2)
        if time.time() - sampleTime > 0.25:
            #print("Ch 0:", round(math.mean(adc_0_list), 3), "V Ch 1:", round(math.mean(adc_1_list), 3), "V")
            #adc_0_list = []
            #adc_1_list = []
            adc_0_list_added = len(adc_0_list) - adc_0_list_old
            adc_1_list_added = len(adc_1_list) - adc_1_list_old
            sampleTime = time.time()
            if len(adc_0_list) > 10*(adc_0_list_added):
                adc_0_list = adc_0_list[adc_0_list_added:]
            if len(adc_1_list) > 10*(adc_1_list_added):
                adc_1_list = adc_1_list[adc_1_list_added:]
            print("Ch 0:", round(math.mean(adc_0_list), 3), "V Ch 1:", round(math.mean(adc_1_list), 3), "V")
            adc_0_list_old = len(adc_0_list)
            adc_1_list_old = len(adc_1_list)

finally:
    GPIO.cleanup()