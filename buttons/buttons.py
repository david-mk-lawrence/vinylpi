import time

import RPi.GPIO as GPIO
import urllib3

PREV = 23
PAUSE = 24
NEXT = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(PREV, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PAUSE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(NEXT, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def listen(api_url):
    try:
        prev_state, pause_state, next_state = False, False, False
        while True:
            prev_state = handle_input(PREV, prev_state, api_url + "/playback/prev")
            pause_state = handle_input(PAUSE, pause_state, api_url + "/playback/toggle")
            next_state = handle_input(NEXT, next_state, api_url + "/playback/next")
            time.sleep(0.2)
    finally:
        GPIO.cleanup()

def handle_input(pin, last_state, url):
    if GPIO.input(pin) == False:
        if not last_state:
            send_state(url)
        return True
    else:
        return False

def send_state(url):
    try:
        http = urllib3.PoolManager()
        resp = http.request("PUT", url)
        if resp.status != 200:
            raise Exception("failed to send state")
    except Exception as err:
        print(err)
