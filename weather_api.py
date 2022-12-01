#!/usr/bin/env python3
import os
import requests
import json

from datetime import datetime
from confluent_kafka import Producer
from pprint import pprint

if __name__ == "__main__":
  KAFKA_IP = os.getenv("KAFKA_IP", "localhost")

  object_keys = (
    "temperature_2m",
    "relativehumidity_2m",
    "apparent_temperature",
    "rain",
    "visibility"
  )

  current_date = datetime.now().strftime("%Y-%m-%d")

  url = f"https://api.open-meteo.com/v1/forecast?latitude=48.85&longitude=2.35&hourly={','.join([key for key in object_keys])}&start_date={current_date}&end_date={current_date}"

  res = requests.get(url)
  res_json = res.json()

  formated_datas = dict(zip(res_json["hourly"]["time"], [dict(zip(object_keys, hourly_datas)) for hourly_datas in zip(*[res_json["hourly"][key] for key in object_keys])]))

  p = Producer({ "bootstrap.servers": KAFKA_IP + ":9092" })

  for time, data in formated_datas.items():
    p.produce("weather", json.dumps({ "time": time, **data }).encode("utf-8"))
  
  p.flush()
