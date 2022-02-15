import smbus

bus = smbus.SMBus(1)
DEVICE_ADDRESS = 0x36      #7 bit address (will be left shifted to add the read>
DEVICE_REG_MODE1 = 0x00
DEVICE_REG_LEDOUT0 = 0x1d

def ReadRawAngle():

    #7:0 - bits
    lowbyte = bus.read_byte_data(DEVICE_ADDRESS, 0x0D)
        
    #11:8 - 4 bits
    highbyte = bus.read_byte_data(DEVICE_ADDRESS,0x0C)
    
    #4 bits have to be shifted to its proper place as we want to build a 12-bit number
    highbyte = highbyte << 8 #shifting to left
    #What is happening here is the following: The variable is being shifted by 8 bits to the left:
    #Initial value: 00000000|00001111 (word = 16 bits or 2 bytes)
    #Left shifting by eight bits: 00001111|00000000 so, the high byte is filled in
    
    #Finally, we combine (bitwise OR) the two numbers:
    #High: 00001111|00000000
    #Low:  00000000|00001111
    #      -----------------
    #H|L:  00001111|00001111
    rawAngle = highbyte | lowbyte; #int is 16 bits (as well as the word)

    #We need to calculate the angle:
    #12 bit -> 4096 different levels: 360° is divided into 4096 equal parts:
    #360/4096 = 0.087890625
    #Multiply the output of the encoder with 0.087890625
    degAngle = rawAngle * 0.087890625; 
    
    #Serial.print("Deg angle: ");
    #Serial.println(degAngle, 2); #absolute position of the encoder within the 0-360 circle
    
    print(degAngle)

def main():
    while(True):
        ReadRawAngle()
