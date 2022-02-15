import smbus


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

bus = smbus.SMBus(1)    # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

DEVICE_ADDRESS = 0x36      #7 bit address (will be left shifted to add the read write bit)
DEVICE_REG_MODE1 = 0x00

#Write a single register
test = bus.read_byte_data(DEVICE_ADDRESS, 0x0E)
test2 = bus.read_byte_data(DEVICE_ADDRESS, 0x0F)

#Write an array of registers
print (test,test2)