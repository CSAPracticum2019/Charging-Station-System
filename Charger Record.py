import picamera
from time import sleep


#setup camera
with picamera.PiCamera() as camera:
    camera.start_recording("pythonVideo.h264")
    sleep(5)
    camera.stop_recording()
