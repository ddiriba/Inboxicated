from adafruit_servokit import ServoKit

servo = ServoKit(channels=16)

servo.servo[0].angle = 25

servo.servo[0].angle = 100