# syntax=docker/dockerfile:1
FROM eclipse-mosquitto
WORKDIR /mosquitto
COPY config config
RUN mosquitto_passwd -c -b /mosquitto/config/pwfile client sekret
EXPOSE 1883 8883