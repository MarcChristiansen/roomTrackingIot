from motionSensor.HCSR501 import hcsr501Sensor
from distanceSensor.HCSR05 import hcsr05Sensor

hcsr501 = hcsr501Sensor(25)
hcsr05 = hcsr05Sensor(23, 24)

try:
    while True:
        motion = hcsr501.get_motion()
        distance = hcsr05.get_distance()
        
        print("Motion detected:", motion)
        print("Distance:", distance)
        time.sleep(2)
except KeyboardInterrupt:
    hcsr501.cleanup()
    hcsr05.cleanup()

