FROM python:buster

WORKDIR /app
ADD sensorPublish.py /app/
ADD distanceSensor/HCSR05.py /app/distanceSensor/
ADD motionSensor/HCSR501.py /app/motionSensor/

ADD requirements.txt /app/
RUN pip3 install -r requirements.txt

CMD [ "python3", "sensorPublish.py" ]