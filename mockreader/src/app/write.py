import argparse
import os
import json


def write(data_file):
    if not os.path.exists(data_file):
        with open(data_file) as f:
            json.dump({}, f, indent=2)

    while True:
        try:
            chip_id = get_chip_id()
            uri = get_uri()
            write_uri(data_file, chip_id, uri)
        except Exception as err:
            print(err)

def get_chip_id():
    try:
        print("Waiting for chip...")
        chip_id = input()
        print(f"Read Chip ID={chip_id}")
        return chip_id
    except Exception as err:
        raise Exception(f"Failed to read chip: {err}")

def get_uri():
    return input("Spotify URI: ")

def write_uri(data_file, chip_id, uri):
    with open(data_file, "r") as f:
        uris = json.load(f)
    uris[chip_id] = uri
    with open(data_file, "w") as f:
        json.dump(uris, f, indent=2)
