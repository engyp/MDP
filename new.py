from picamera import PiCamera
import time

camera = PiCamera()
camera.resolution = (640,480)
camera.framerate = 90
camera.video_stabilization = True
camera.shutter_speed = 4000
camera.ISO = 800
camera.brightness = 55

camera.start_preview()
time.sleep(2)

camera.start_recording("my_movie.h264")
time.sleep(5)
camera.stop_recording()