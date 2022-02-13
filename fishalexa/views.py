from django.shortcuts import render
from django.http import StreamingHttpResponse, HttpResponse
import cv2, threading, time, serial
from django.views.decorators.csrf import ensure_csrf_cookie
import RPi.GPIO as GPIO

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        image = cv2.resize(image, (image.shape[1]//2,image.shape[0]//2))
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@ensure_csrf_cookie
def index(request):
    return render(request, 'fishalexa/home.html')

def video_stream(request):
    return StreamingHttpResponse(gen(VideoCamera()),
                    content_type='multipart/x-mixed-replace; boundary=frame')


def ser_comm(str):
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout = 1)
    ser.reset_input_buffer()
    cmd = str + '\n'
    ser.write(cmd.encode('utf-8'))
    line = ser.readline().decode('utf-8').rstrip()
    time.sleep(1)
    print(line)

def feed(request):
    print('feed')
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(13,GPIO.OUT)
    servo1 = GPIO.PWM(13,50)
    servo1.start(0)
    servo1.ChangeDutyCycle(3)
    time.sleep(.10682)
    servo1.ChangeDutyCycle(0)
    servo1.stop()
    return HttpResponse()

def light_on(request):
    print(request)
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(18,GPIO.OUT)
    GPIO.output(18,GPIO.HIGH)
    return HttpResponse()

def light_off(request):
    print(request)
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(18,GPIO.OUT)
    GPIO.output(18,GPIO.LOW)
    return HttpResponse()
