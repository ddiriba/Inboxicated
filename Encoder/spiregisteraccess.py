import smbus

bus = smbus.SMBus(1)    # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

DEVICE_ADDRESS = 0x36      #7 bit address (will be left shifted to add the read write bit)
DEVICE_REG_MODE1 = 0x00

#Write a single register
test = bus.read_byte_data(DEVICE_ADDRESS, 0x0C)

#Write an array of registers
print (test)