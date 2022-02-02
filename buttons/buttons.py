import time

import RPi.GPIO as GPIO
import urllib3

PREV = 23
PAUSE = 24
NEXT = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(PREV, GPIO.IN, pull_up_down=GPIO.PUD_UP) # prev
GPIO.setup(PAUSE, GPIO.IN, pull_up_down=GPIO.PUD_UP) # pause
GPIO.setup(NEXT, GPIO.IN, pull_up_down=GPIO.PUD_UP) # next

http = urllib3.PoolManager()

def listen(api_url):
    try:
        while True:
            input_state = GPIO.input(PREV)
            if input_state == False:
                print('Prev Pressed')
                send_state(api_url + "/playback/prev")
            input_state = GPIO.input(PAUSE)
            if input_state == False:
                print('Pause Pressed')
                send_state(api_url + "/playback/toggle")
            input_state = GPIO.input(NEXT)
            if input_state == False:
                send_state(api_url + "/playback/next")

            time.sleep(0.2)
    finally:
        GPIO.cleanup()

def send_state(url):
    http.request("PUT", url)
