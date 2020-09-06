from picamera import PiCamera
import time

camera = PiCamera()

camera.start_preview()

time.sleep(10)

camera.stop_preview()

# camera.start_recording("my_movie.h264")
# time.sleep(5)
# camera.stop_recording()