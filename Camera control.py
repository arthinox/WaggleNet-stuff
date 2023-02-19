from picamera import PiCamera
import time
from time import sleep
import datetime

id = datetime.datetime.now().strftime("%y-%m-%d-%H:%M:%S")
filename = "/home/pi/Desktop/"+id+".jpg"
camera = PiCamera()

camera.start_preview()
sleep(10)
camera.capture(filename)
camera.stop_preview()