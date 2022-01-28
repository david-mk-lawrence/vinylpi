import json
import urllib3


def read(api_url, data_file):
    while True:
        try:
            chip_id = get_chip_id()
            uri = get_uri(data_file, chip_id)
            send_uri(api_url, uri)
        except Exception as err:
            print(err)

def get_chip_id():
    try:
        print("Waiting for chip...")
        chip_id = input()
        print(f"Read Chip ID={id}")
        return chip_id
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

    resp = http.request("PUT", api_url, body=body, headers={"content-type": "application/json"})
    if resp.status != 200:
        raise Exception("failed to send uri")
