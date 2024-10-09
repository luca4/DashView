import threading
import asyncio
import os
from time import sleep
from .custom_timer import CustomTimer

import paho.mqtt.client as mqtt
import platform

from loguru import logger



if os.getenv("DEPLOY_TYPE") == "PROD":
    import RPi.GPIO as GPIO 
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)


class TempSensor:
    import smbus2
    import bme280
    
    
    def __init__(self) -> None:
        if os.getenv("DEPLOY_TYPE") == "PROD":
            self.address = 0x76
            self.bus = self.smbus2.SMBus(bus_number = 1)

    def _get_ambient_data(self):
        if not os.getenv("DEPLOY_TYPE") == "PROD":
            return {'temperature': 11.11, 'humidity': 11.11}
        
        calibration_params = self.bme280.load_calibration_params(self.bus, self.address)
        sensor_data = self.bme280.sample(self.bus, self.address, calibration_params)
        return { "temperature": f'{sensor_data.temperature:.2f}', "humidity": f'{sensor_data.humidity:.2f}' }


    def _send_ambient_data(self):
        from . import sio
        while True:
            async def emit(event, msg):
                await sio.emit(event, msg)
                logger.debug(f"Emitting ambient data. Event: {event}, Data: {str(msg)}")

            data = self._get_ambient_data()
            asyncio.run(emit("ambientData", data))
            sleep(10)
            

    def start_sending_ambient_data(self):
        threading.Thread(target=self._send_ambient_data, daemon=True).start()


class Heater:
    pin = 31
    if os.getenv("DEPLOY_TYPE") == "PROD":
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.OUT)

    def __init__(self):
        self.timer = CustomTimer()
        self.emitter_thread = None
        self.is_on = False

    def turn_on(self, minutes: int):
        self.is_on = True
        if os.getenv("DEPLOY_TYPE") == "PROD":
            GPIO.output(Heater.pin, GPIO.HIGH)

        logger.debug(f"Heater - turn on for {minutes} minutes")

        self.timer.start(minutes * 60, self.turn_off)
        if self.emitter_thread is None:
            self.emitter_thread = threading.Thread(target=self._emit_remaining_time, daemon=True)
            self.emitter_thread.start()

    def turn_off(self):
        self.is_on = False
        if os.getenv("DEPLOY_TYPE") == "PROD":
            GPIO.output(Heater.pin, GPIO.LOW)
        
        logger.debug("Heater - turn off")
        self.timer.stop()

        self.emitter_thread = None
        

    def _emit_remaining_time(self):
        from . import sio
        while True:
            if not self.is_on:
                break

            async def emit(event, msg):
                await sio.emit(event, msg)
                logger.debug(f"Heater - emitting remaining time. Event: {event}, Data: {str(msg)}")

            data = self.timer.get_remaining_minutes()
            asyncio.run(emit("remainingHeaterMinutes", data))
            sleep(10)



heater = Heater()
temp_sensor = TempSensor()

