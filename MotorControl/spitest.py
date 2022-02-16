import smbus

bus = smbus.SMBus(1)  #i2c bus number of gpio pins is 1
DEVICE_ADDRESS = 0x36  #address of i2c device, AS5600 (sudo i2cdetect -y 1) (1 is the i2c bus number)


class Encoder():
    def ReadRawAngle():

        # 7:0 - 4 bits
        lowbyte = bus.read_byte_data(DEVICE_ADDRESS, 0x0D) #address from AS5600 Datasheet -> https://ams.com/en/as5600#tab/documents
            
        # 11:8 - 4 bits
        highbyte = bus.read_byte_data(DEVICE_ADDRESS,0x0C)
        
        # bits have to be shifted to its proper place as we want to build a 12-bit number
        highbyte = highbyte << 8 # bitshift to left by 8 digits
        #The variable is being shifted by 8 bits to the left:
        rawAngle = highbyte | lowbyte; 
        
        # 12 bit -> 4096 different levels: 360 is divided into 4096 equal parts:
        # 360/4096 = 0.087890625
        # Multiply the output by 0.087890625
        
        degAngle = rawAngle * 0.087890625;     
        print(degAngle)
        return(degAngle)

def main():
    
    encode = Encoder()
    while(True):
        encode.ReadRawAngle()
    
if __name__ == '__main__':
    main()
