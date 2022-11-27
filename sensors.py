#!/usr/bin/env python3
import os
import json
import serial
from confluent_kafka import Producer

FAKE = os.getenv("FAKE") is not None
DATA_KEYS = ["humidite", "luminosite", "temperature"]

def get_values(serial_port):
  row = serial_port.readline().decode("utf-8").strip()
  return [float(x) if '.' in x else int(x) for x in row.split(",")]

def generate_random_values(_):
  import random as rand
  from time import sleep
  sleep(1)
  return [
    round(rand.uniform(60, 80), 1),
    rand.randint(300, 400),
    round(rand.uniform(15, 21), 1),
    rand.randint(800, 1024)
  ]

if __name__ == "__main__":
  p = Producer({ "bootstrap.servers": "159.65.16.140:9092" })
  ser = serial.Serial("/dev/cu.usbserial-10", 9600) if not FAKE else None
  fetcher = get_values if not FAKE else generate_random_values

  while True:
    data = dict(zip(DATA_KEYS, fetcher(ser)))
    print(data)
    p.produce("air", json.dumps(data).encode("utf-8"))
    p.flush()
