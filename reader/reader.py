import json
import time

import RPi.GPIO as GPIO
import urllib3
from mfrc522 import SimpleMFRC522


def read(api_url, data_file):
    rfid = SimpleMFRC522()

    try:
        while True:
            try:
                chip_id = get_chip_id(rfid)
                uri = get_uri(data_file, chip_id)
                send_uri(api_url, uri)
            except Exception as err:
                print(err)
            time.sleep(2)
    finally:
        GPIO.cleanup()

def get_chip_id(rfid):
    try:
        print("Waiting for chip...")
        chip_id, _ = rfid.read()
        print(f"Read Chip ID={chip_id}")
        return str(chip_id)
    except Exception as err:
        raise Exception(f"Failed to read chip: {err}")

def get_uri(data_file, chip_id):
    try:
        with open(data_file) as f:
            uris = json.load(f)
        return uris[chip_id]
    except KeyError:
        raise Exception("key not found in data file. chip needs to be written first")

def send_uri(api_url, uri):
    http = urllib3.PoolManager()
    body = json.dumps({"uri": uri}).encode("utf-8")

    resp = http.request("PUT", api_url + "/playback/play", body=body, headers={"content-type": "application/json"})
    if resp.status != 200:
        raise Exception("failed to send uri")
