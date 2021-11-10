import RPi.GPIO as GPIO

class hcsr501Sensor(object):
    def __init__(self, GPIO_PIR):
        self.GPIO_PIR = GPIO_PIR
        GPIO.setup(self.GPIO_PIR, GPIO.IN)

    def get_motion(self):
        #If HC-SR501 pin is HIGH, motions is detected
        motion = GPIO.input(self.GPIO_PIR) == 1  
        return motion
        
    def cleanup(self):
        GPIO.cleanup(self.GPIO_PIR)