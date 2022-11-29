#!/usr/bin/env python3
import requests

from pprint import pprint

if __name__ == "__main__":
  url = "https://api.open-meteo.com/v1/forecast?latitude=48.85&longitude=2.35&hourly=temperature_2m,relativehumidity_2m"
  res = requests.get(url)
  data = res.json()
  pprint(dict(zip(data["hourly"]["time"], zip(data["hourly"]["temperature_2m"], data["hourly"]["relativehumidity_2m"]))))

